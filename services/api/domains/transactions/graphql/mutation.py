import strawberry
from strawberry.types import Info

from api.broker import rabbit_connection
from shared.schemas import MessageSchema
from ..bl import TransactionBL
from api.utils.graphql import IsAuthenticated


@strawberry.type
class TransactionMutations:
    @strawberry.mutation(
        description='Confirm transaction',
        permission_classes=[IsAuthenticated]
    )
    async def confirm_transaction(
            self,
            order_id: int,
            info: Info
    ) -> None:
        """ Confirm payment public order """
        data = await TransactionBL(info).confirm(order_id)
        await rabbit_connection.send_messages(MessageSchema(
            action='payment:check',
            body=data
        ))
