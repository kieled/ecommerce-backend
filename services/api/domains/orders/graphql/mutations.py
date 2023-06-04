import strawberry
from strawberry.types import Info

from ..types import UpdateOrderInput, CreatedOrderIdType
from ..bl import OrderBL

from api.utils.graphql import IsAdmin, add_random_temp_id_for_response
from api.domains.addresses import AddressBL
from api.domains.requisite import RequisiteBL
from api.domains.transactions.features.promo import PromoBL
from api.domains.transactions import TransactionBL
from api.domains.products import ProductBL
from ...addresses.types import AddressInput


@strawberry.type
class OrderMutations:
    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Update order info'
    )
    async def update_order(
            self,
            order: UpdateOrderInput,
            info: Info
    ) -> None:
        """ Update order mutation """
        return await OrderBL(info).update(order)

    @strawberry.mutation(
        description='Create new order'
    )
    async def create_order(
            self,
            payload: AddressInput,
            info: Info
    ) -> CreatedOrderIdType:
        """ Create order from cart """
        temp_user_id = add_random_temp_id_for_response(self.info)
        payload.address_id = await AddressBL(info).get_or_create(payload, temp_user_id)
        promo = None
        if payload.promo:
            promo = await PromoBL(info).find(payload.promo)
        requisite = await RequisiteBL(info).get_active(payload.payment_type)
        if not requisite:
            raise Exception('No requisites are available')
        amount = await ProductBL(info).calc_prices(payload.products)
        transaction_id = await TransactionBL(info).create(amount, requisite.id, promo)
        data = await OrderBL(info).create(payload, transaction_id)

        return CreatedOrderIdType(id=data['id'])
