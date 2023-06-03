import os
from importlib import import_module
from typing import Callable, Optional, get_type_hints


class Router:
    _routes: dict[str, dict[str, Callable[..., any]]] = {}

    def __init__(self):
        modules = list(filter(
            lambda x: x != '__init__',
            map(lambda y: y.split('.')[0], os.listdir('tasks'))
        ))
        for module in modules:
            imported = import_module(f'tasks.{module}')
            if not hasattr(imported, '__all__'):
                continue
            self._routes[module] = {i: getattr(imported, i) for i in imported.__all__}

    def get_method(self, action: str) -> Optional[Callable[..., any]]:
        module = action.split(':')[0]
        method = action.split(':')[1]
        if self._exists(module, method):
            return self._routes.get(module).get(method)

    @staticmethod
    def check_args(func: Callable, data: dict) -> bool:
        for arg, arg_type in get_type_hints(func).items():
            if arg not in data:
                return False
            if not isinstance(data[arg], arg_type):
                return False
        return True

    def _exists(self, module: str, method: str):
        if hasattr(self._routes, module) and hasattr(self._routes.get(module), method):
            return True
        return False


router = Router()
