import logging
import re
from api.utils import DictSearch
import aiohttp
from api.schemas import ProductParsedType, ProductParsedColorType, ProductParsedParamsType
import json
from urllib.parse import parse_qs, urlparse

needed_params = ['Сезон', 'Материал', 'Плотность ткани', 'Season', 'season']

api_url = 'https://wapi.aliexpress.ru/mobile-layout/pdp-v2'

headers = {
    'User-Agent': 'ali-android-13-567-8.20.341.823566',
    'x-aer-client-type': 'android',
    'x-aer-lang': 'en_RU',
    'x-aer-currency': 'RUB',
    'x-aer-ship-to-country': 'RU',
    'x-appkey': 'XXXXXXXX',
    'accept': 'application/json',
    'x-aer-device-id': 'X0XXxX+Xxx0XXX0XxxXXxx0X'
}


def get_param(names: list[str], params):
    try:
        return [i for i in params if i['name'] in names][0]['values']
    except Exception as e:
        logging.error(e)
        return []


def find_item(items: list[dict], key: str | None = None, value: str | None = None):
    for i in items:
        for k, v in i.items():
            if key and value:
                if (k == key) and (v == value):
                    return i
            elif key:
                if k == key:
                    return i
            else:
                if v == value:
                    return i
    return None


async def aliexpress_parser(url: str) -> ProductParsedType:
    if 'aliexpress.ru' not in url:
        raise Exception('Invalid Aliexpress URL')
    async with aiohttp.ClientSession(headers=headers) as session:
        if 'https://sl.aliexpress.ru/' in url:
            async with session.get(url, allow_redirects=False) as response:
                url = response.headers['Location']
        body = {
            'productId': re.findall(r'\d+.html', url)[0].split('.')[0]
        }
        async with session.post(api_url, data=body) as page:
            json_data = await page.json()
    current = DictSearch(json_data)

    params_block = current.cut_path([i for i in current.search("PdpSku") if i.split(".")[-1] == "name"][0], 1)

    params = current.get_value(f'{params_block}.state.data.properties')
    params_sku = current.get_value(f'{params_block}.state.data.propertyValuesToSkuIds')
    sizes = get_param(['Size', 'Размер'], params)
    colors = get_param(['Color', 'Цвет'], params)

    sizes_ids = [s['id'] for s in sizes]
    colors_ids = [c['id'] for c in colors]

    param_ids = [k for k, v in params_sku.items()][0].split(',')

    def find_index(items: list[str]):
        for index, i in enumerate(param_ids):
            if i in items:
                return index
        return None

    size_index = find_index(sizes_ids)
    color_index = find_index(colors_ids)

    available = {}

    sku_info = current.get_value(f'{current.cut_path(current.search("PdpBottomBar"), 1)}.state.data.skuInfos')

    for k, v in params_sku.items():
        color_id = k.split(',')[color_index]
        if size_index is not None:
            size_id = k.split(',')[size_index]
        else:
            size_id = None
        sku_id = v
        if sku_id in sku_info.keys() and int(sku_info[sku_id]['quantityInStock']) > 0:
            if size_id:
                if available.get(color_id):
                    available[color_id].append(size_id)
                else:
                    available[color_id] = [size_id]
            else:
                available[color_id] = []

    images = [i['imageUrl'] for i in current.get_value(current.search('generalImgList', True))]
    sku_images = current.get_value(current.search('skuImgList', True))

    result_colors = []

    for color in colors:
        if color['id'] in available.keys():
            color_sizes: list[str] = [size['title'] for size in sizes if size['id'] in available[color['id']]]
            parsed_sizes = []
            for size in color_sizes:
                if size.startswith('Asian '):
                    parsed_sizes.append(size.replace('Asian ', ''))
                else:
                    parsed_sizes.append(size)
            result_colors.append(ProductParsedColorType(
                name=color['title'],
                image=find_item(sku_images, 'skuPropertyValueId', color['id']).get('imageUrl'),
                sizes=parsed_sizes
            ))

    params = json.loads(parse_qs(urlparse(current.get_value(
        f'{current.cut_path(current.search("ProductSpecification"), 1)}.state.data.onClickUrl')).query)['props'][0])
    params = [ProductParsedParamsType(
        name=i['attrName'],
        value=i['attrValue']
    ) for i in params if i['attrName'] in needed_params]

    return ProductParsedType(
        colors=result_colors,
        images=images,
        params=params,
        url=url.split('?')[0]
    )
