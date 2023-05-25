import strawberry
from strawberry.types import Info
from celery_app import add_post_instagram_task, edit_description_instagram_task
from config import session
from parsers import prices_manager
from schemas import ProductCreateInput, ProductUpdateInput, CreatedProductType, \
    CreatedProductImageType
from services import ProductService
from utils import IsAdmin, get_dict_object


@strawberry.type
class ProductMutation:
    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Create new product (need fetch on the client firstly)'
    )
    async def create_product(
            self,
            product: ProductCreateInput,
            info: Info
    ) -> CreatedProductType:
        async with session() as s:
            product_id = await ProductService(s, info).create(product)
        async with session() as s:
            data = await ProductService(s, info).detail_full(product_id)
            # add_post_instagram_task.apply_async(args=[
            #     get_dict_object(data),
            #     await prices_manager.get()
            # ])
        return CreatedProductType(
            id=data.id,
            images=[CreatedProductImageType(
                id=image.id,
                path=image.path
            ) for image in data.images]
        )

    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Update product info'
    )
    async def update_product(
            self,
            product: ProductUpdateInput,
            info: Info
    ) -> None:
        async with session() as s:
            await ProductService(s, info).update(product)
        # async with session() as s:
        #     updated_product = await ProductService(s, info).detail_full(product.product_id)
        #     if updated_product.inst_url:
        #         edit_description_instagram_task.apply_async(args=[
        #             get_dict_object(updated_product),
        #             await prices_manager.get()
        #         ])

    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Delete product'
    )
    async def delete_product(
            self,
            product_id: int,
            info: Info
    ) -> None:
        async with session() as s:
            await ProductService(s, info).delete(product_id)
