from typing import Generator

from .storages import client_storage


def get_clients() -> Generator:
    with client_storage as c:
        yield c
