import strawberry
from .transactions import TransactionQuery
from .products import ProductQuery
from .users import UserQuery
from .requisites import RequisitesQuery
from .public import PublicQuery
from .product_categories import ProductCategoryQuery
from .customers import CustomerQuery
from .location import LocationQuery
from .orders import OrderQuery


@strawberry.type
class Query(UserQuery, ProductQuery, RequisitesQuery, TransactionQuery, PublicQuery, ProductCategoryQuery, CustomerQuery,
            LocationQuery, OrderQuery):
    pass


__all__ = ['Query']
