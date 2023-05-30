from collections import defaultdict

from api.schemas import ProductParsedType, ProductParsedColorType, ProductParsedParamsType
import json
from urllib.parse import parse_qs, urlparse
from api.utils.aliexpress import DictSearch, find_index, find_item, get_param, fetch_product_json


def _prepare_available(current: DictSearch, sizes: list, colors: list, params_block: str):
    params_sku = current.get_value(f'{params_block}.state.data.propertyValuesToSkuIds')
    param_ids = [k for k, v in params_sku.items()][0].split(',')
    size_index = find_index([s['id'] for s in sizes], param_ids)
    available = defaultdict(list)
    sku_info = current.get_value(
        f'{current.cut_path(current.search("PdpBottomBar"), 1)}.state.data.skuInfos'
    )
    for k, v in params_sku.items():
        color_id = k.split(',')[find_index([c['id'] for c in colors], param_ids)]
        if size_index is not None:
            size_id = k.split(',')[size_index]
        else:
            size_id = None
        sku_id = v
        if sku_id in sku_info.keys() and int(sku_info[sku_id]['quantityInStock']) > 0:
            available[color_id].append(size_id)
    return available


def _prepare_colors(current: DictSearch, colors: list, available: defaultdict, sizes: list):
    sku_images = current.get_value(current.search('skuImgList', True))

    for color in colors:
        if color['id'] in available:
            color_sizes: list[str] = [size['title'] for size in sizes if size['id'] in available[color['id']]]
            parsed_sizes = []
            for size in color_sizes:
                if size.startswith('Asian '):
                    parsed_sizes.append(size.replace('Asian ', ''))
                else:
                    parsed_sizes.append(size)
            yield ProductParsedColorType(
                name=color['title'],
                image=find_item(sku_images, 'skuPropertyValueId', color['id']).get('imageUrl'),
                sizes=parsed_sizes
            )


async def aliexpress_parser(url_or_id: str) -> ProductParsedType:
    current = DictSearch(await fetch_product_json(url_or_id))

    params_block = current.cut_path([i for i in current.search("PdpSku") if i.split(".")[-1] == "name"][0], 1)
    params = current.get_value(f'{params_block}.state.data.properties')

    sizes = get_param(['Size', 'Размер'], params)
    colors = get_param(['Color', 'Цвет'], params)

    images = [i['imageUrl'] for i in current.get_value(current.search('generalImgList', True))]

    params = json.loads(parse_qs(urlparse(current.get_value(
        f'{current.cut_path(current.search("ProductSpecification"), 1)}.state.data.onClickUrl')).query)['props'][0])
    needed_params = ['Сезон', 'Материал', 'Плотность ткани', 'Season', 'season']
    params = [ProductParsedParamsType(
        name=i['attrName'],
        value=i['attrValue']
    ) for i in params if i['attrName'] in needed_params]

    return ProductParsedType(
        colors=_prepare_colors(
            current=current,
            colors=colors,
            available=_prepare_available(
                current=current,
                sizes=sizes,
                colors=colors,
                params_block=params_block
            ),
            sizes=sizes
        ),
        images=images,
        params=params,
        url=url_or_id.split('?')[0]
    )
