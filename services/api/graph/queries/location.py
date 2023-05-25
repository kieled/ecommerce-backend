import strawberry
from parsers import location_service
from schemas import LocationType


@strawberry.type
class LocationQuery:
    @strawberry.field(
        description='Get info about location from query'
    )
    async def location_search(self, query: str) -> list[LocationType]:
        return await location_service.search(query)

    @strawberry.field(
        description='Get info about location from lat and lon'
    )
    async def location_reverse(
            self, lat: str, lon: str
    ) -> LocationType:
        return await location_service.reverse(lat, lon)
