import strawberry
from alchemy_graph import get_dict_object
from strawberry.types import Info

from api.broker import rabbit_connection
from shared.schemas import MessageSchema
from ..types import ProductCreateInput, ProductUpdateInput, CreatedProductType, \
    CreatedProductImageType
from ..bl import ProductBL
from ...users.features.auth import IsAdmin


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
        product_id = await ProductBL(info).create(product)
        data = await ProductBL(info).detail_full(product_id)
        await rabbit_connection.send_messages([
            MessageSchema(
                action='instagram:add',
                body={
                    'data': get_dict_object(data)
                }
            )
        ])
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
        await ProductBL(info).update(product)
        updated_product = await ProductBL(info).detail_full(product.product_id)
        if updated_product.inst_url:
            await rabbit_connection.send_messages([
                MessageSchema(
                    action='instagram:edit',
                    body={
                        'data': get_dict_object(updated_product)
                    }
                )
            ])

    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Delete product'
    )
    async def delete_product(
            self,
            product_id: int,
            info: Info
    ) -> None:
        await ProductBL(info).delete(product_id)
