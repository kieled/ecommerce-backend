import re
from dataclasses import dataclass


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
