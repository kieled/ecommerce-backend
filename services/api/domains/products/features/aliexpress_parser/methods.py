from collections import defaultdict

from .types import ProductParsedColorType
from .utils import DictSearch, find_index, find_item


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
