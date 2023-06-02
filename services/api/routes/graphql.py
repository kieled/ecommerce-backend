import strawberry
from strawberry.django.apps import StrawberryConfig
from strawberry.fastapi import GraphQLRouter

from api.domains.users.features.auth import get_auth_context

from api.domains.addresses.graphql import AddressQuery
from api.domains.users.graphql import UserQuery, UserMutation


@strawberry.type
class Query(AddressQuery, UserQuery):
    ...


@strawberry.type
class Mutation(UserMutation):
    ...


strawberry_config = StrawberryConfig(auto_camel_case=True)
schema = strawberry.Schema(Query, Mutation, config=strawberry_config)
router = GraphQLRouter(schema, context_getter=get_auth_context, graphiql=True)
