from fastapi import FastAPI, Form, HTTPException, status
from payment.services import yandex_service

app = FastAPI(redoc_url=None, docs_url=None, openapi_url=None, title='Payment Service')


@app.post('/check')
def check_payment(
        amount: int = Form(...),
        latest_ids: list[str] = Form([])
):
    result = [i.operation_id for i in yandex_service.find_operation(amount)]
    for i in result:
        if i not in latest_ids:
            return dict(
                transaction_id=i
            )
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Transaction not found')
