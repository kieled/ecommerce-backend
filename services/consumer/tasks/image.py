import os


def delete(path: str):
    os.remove(path)


__all__ = ['delete']
