import aiohttp
from .types import LocationType, LocationAddressType


class LocationService:
    def __init__(self):
        self.url = 'https://nominatim.openstreetmap.org'
        self.params = {
            'format': 'json',
            'accept-language': 'ru'
        }

    @staticmethod
    def _get_type_from_dict(data: dict):
        address = data.get('address')
        filtered_address = {}
        for k in address.keys():
            if k in LocationAddressType.__annotations__ and address.get(k) is not None:
                filtered_address[k] = address.get(k)
        del address
        filtered_address['state'] = filtered_address.get('state') if filtered_address.get(
            'state') else filtered_address.get('city')
        if filtered_address['state'] is None:
            del filtered_address['state']
        return LocationType(
            display_name=data.get('display_name'),
            address=LocationAddressType(**filtered_address)
        )

    async def search(self, query: str) -> list[LocationType]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.url}/search', params={
                **self.params,
                'addressdetails': '1',
                'limit': '3',
                'q': query
            }) as data:
                result = await data.json()
        return [self._get_type_from_dict(item) for item in result]

    async def reverse(self, lat: str, lon: str) -> LocationType:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.url}/reverse', params={
                **self.params,
                'lon': lon,
                'lat': lat
            }) as data:
                result = await data.json()
        return self._get_type_from_dict(result)


location_service = LocationService()
