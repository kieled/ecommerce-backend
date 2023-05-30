import random
import string
import re
from dataclasses import dataclass

import aiohttp


def get_param(names: list[str], params: list):
    try:
        return [i for i in params if i['name'] in names][0]['values']
    except ValueError:
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


def random_generation(input_string: str) -> str:
    result = ''
    replacements = {
        'x': string.ascii_lowercase,
        'X': string.ascii_uppercase,
        '0': string.digits
    }
    for char in input_string:
        if char in replacements:
            result += random.choice(replacements[char])
        else:
            result += char
    return result


def find_index(items: list[str], data: list[str]):
    for index, i in enumerate(data):
        if i in items:
            return index
    return None


@dataclass
class DictSearch:
    input_item: dict

    def search(self, search_value: str, search_by_key: bool = False, partial: bool = False):
        results = []

        def process(data, path: str):
            if not isinstance(data, dict):
                return None
            for key, value in data.items():
                if search_by_key:
                    if key == search_value:
                        results.append(f'{path}.{key}')
                prefix = '.' if path != '' else ''
                if isinstance(value, dict):
                    process(data.get(key), f'{path}{prefix}{key}')
                if isinstance(value, list):
                    for index, i in enumerate(value):
                        process(i, f'{path}{prefix}{key}[{index}]')
                else:
                    if partial and isinstance(value, str):
                        if search_value in value:
                            results.append(f'{path}{prefix}{key}')
                    if search_value == value:
                        results.append(f'{path}{prefix}{key}')

        process(self.input_item, '')

        return results[0] if len(results) == 1 else results

    def get_value(self, path: str):
        path_iter = path.split('.')

        def process(current, item):
            lists = re.findall(r'[\d+]+', current)
            key = re.findall('[a-zA-Z]+', current)[0]
            if len(lists):
                return item.get(key)[int(lists[0])]
            else:
                return item.get(current)

        res = self.input_item

        for i in path_iter:
            res = process(i, res)
        return res

    @staticmethod
    def cut_path(path: str, count: int):
        process = path.split('.')[:-count]
        return '.'.join(process)


headers = {
    'User-Agent': 'ali-android-13-567-8.20.341.823566',
    'x-aer-client-type': 'android',
    'x-aer-lang': 'en_RU',
    'x-aer-currency': 'RUB',
    'x-aer-ship-to-country': 'RU',
    'x-appkey': random_generation('XXXXXXXX'),
    'accept': 'application/json',
    'x-aer-device-id': random_generation('X0XXxX+Xxx0XXX0XxxXXxx0X')
}


async def fetch_product_json(url: str) -> dict | None:
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            if 'https://sl.aliexpress.ru/' in url:
                async with session.get(url, allow_redirects=False) as response:
                    url_or_id = response.headers['Location']
            if 'https://' in url_or_id:
                url_or_id = re.findall(r'\d+.html', url_or_id)[0].split('.')[0]
            async with session.post(
                    'https://wapi.aliexpress.ru/mobile-layout/pdp-v2',
                    data={
                        'productId': url_or_id
                    }
            ) as page:
                return await page.json()
    except Exception as e:
        print(e)
        return None
