import strawberry
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig

from api.domains.addresses.graphql import AddressQuery
from api.domains.categories.graphql import ProductCategoryQuery, ProductCategoryMutation
from api.domains.orders.graphql import OrderQuery, OrderMutations
from api.domains.products.graphql import ProductQuery, ProductMutation
from api.domains.requisite.graphql import RequisitesMutation, RequisitesQuery
from api.domains.requisite_types.graphql import RequisiteTypeQuery, RequisiteTypeMutation
from api.domains.transactions.graphql import TransactionQuery, TransactionMutations
from api.domains.users.graphql import UserQuery, UserMutation


@strawberry.type
class Query(
    AddressQuery,
    UserQuery,
    RequisitesQuery,
    RequisiteTypeQuery,
    ProductCategoryQuery,
    ProductQuery,
    OrderQuery,
    TransactionQuery
):
    ...


@strawberry.type
class Mutation(
    UserMutation,
    TransactionMutations,
    RequisiteTypeMutation,
    RequisitesMutation,
    OrderMutations,
    ProductMutation,
    ProductCategoryMutation
):
    ...


async def get_auth_context(
        auth: AuthJWT = Depends()
):
    try:
        auth.jwt_required()
        user_id = int(auth.get_jwt_subject().split(',')[0])
    except (AuthJWTException, ValueError):
        user_id = None

    return {
        'user_id': user_id
    }


strawberry_config = StrawberryConfig(auto_camel_case=True)
schema = strawberry.Schema(Query, Mutation, config=strawberry_config)
router = GraphQLRouter(schema, context_getter=get_auth_context, graphiql=True)
