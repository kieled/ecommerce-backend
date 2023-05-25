from payment.schemas.yandex import YandexItemSchema
from payment.settings import settings
import requests
from requests import Session


class YandexService:
    def __init__(self):
        self.url: str = 'https://yoomoney.ru/api/operation-history'
        self.headers = {
            'Authorization': f'Bearer {settings.YANDEX_TOKEN}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.result: list[YandexItemSchema] = []

    def _find(self, history: list[YandexItemSchema], amount: int):
        self.result = []

        for i in history:
            if int(i.amount) == amount:
                self.result.append(i)

    def _get_session(self) -> Session:
        s = Session()
        s.headers.update(self.headers)
        return s

    def _history(self):
        res = requests.post(self.url, data={
            'type': 'deposition',
            'records': '2'
        }, headers=self.headers)
        response = res.json()
        return [YandexItemSchema.parse_obj(i) for i in response.get('operations')]

    def find_operation(self, amount: int):
        data = self._history()
        self._find(data, amount)
        return self.result


yandex_service = YandexService()

__all__ = ['yandex_service']
