from instagrapi import Client
from tinydb import TinyDB, Query
import json


class ClientStorage:
    cl: Client
    db = TinyDB('./db.json')

    def init_client(self):
        if not self.cl:
            cl = Client()
            cl.request_timeout = 0.5
            self.cl = cl

    def set(self):
        self.db.truncate()
        self.db.insert({
            'id': 1,
            'settings': json.dumps(self.cl.get_settings())
        })

    def __enter__(self):
        settings = json.loads(self.db.search(Query().id == 1)[0]['settings'])
        self.init_client()
        self.cl.set_settings(settings)
        return self.cl

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...


client_storage = ClientStorage()
