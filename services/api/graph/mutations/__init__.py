import strawberry

from .orders import OrderMutation
from .products import ProductMutation
from .users import UserMutation
from .requisites import RequisitesMutation
from .product_categories import ProductCategoryMutation
from .customers import CustomersMutation


@strawberry.type
class Mutation(UserMutation, ProductMutation, RequisitesMutation, OrderMutation, ProductCategoryMutation,
               CustomersMutation):
    pass


__all__ = ['Mutation']
