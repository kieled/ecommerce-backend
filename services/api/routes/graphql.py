import strawberry
from strawberry.django.apps import StrawberryConfig
from strawberry.fastapi import GraphQLRouter

from api.domains.users.features.auth import get_auth_context

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


strawberry_config = StrawberryConfig(auto_camel_case=True)
schema = strawberry.Schema(Query, Mutation, config=strawberry_config)
router = GraphQLRouter(schema, context_getter=get_auth_context, graphiql=True)
