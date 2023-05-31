import logging
from instagrapi import Client
from tinydb import TinyDB, Query
import json


class ClientStorage:
    db = TinyDB('./db.json')

    def client(self):
        cl = Client()
        cl.request_timeout = 0.5
        return cl

    def get(self) -> Client:
        try:
            settings = json.loads(self.db.search(Query().id == 1)[0]['settings'])
            cl = Client()
            cl.set_settings(settings)
            cl.get_timeline_feed()
            return cl
        except Exception as e:
            logging.error(e.__class__.__name__)
            try:
                settings = json.loads(self.db.search(Query().id == 1)[0]['settings'])
                cl = Client()
                cl.set_settings(settings)
                cl.username = 'distortion.wear'
                cl.password = '9693595kK'
                cl.relogin()
                return cl
            except Exception:
                raise Exception("Error login to Instagram")

    def set(self, cl: Client) -> bool:
        self.db.truncate()
        self.db.insert({'id': 1, 'settings': json.dumps(cl.get_settings())})
        return True

    def close(self):
        pass
