from typing import Generator

from storages import ClientStorage


def get_clients() -> Generator:
    clients = ClientStorage()
    try:
        yield clients
    finally:
        clients.close()
