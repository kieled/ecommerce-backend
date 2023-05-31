from urllib.parse import parse_qs, urlparse
import json

from .types import ProductParsedType, ProductParsedParamsType
from .utils import DictSearch, get_param, fetch_product_json
from .methods import _prepare_available, _prepare_colors


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
