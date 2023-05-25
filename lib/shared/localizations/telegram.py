order_confirmed_message = 'обработан.\n\n✉Как только мы его отправим, вы ' \
                          'получите трек-код для отслеживания.'

new_order_message = 'Новый оплаченный заказ!'


def track_code_message(track_code: str):
    return \
        f'отправлен. \n\n' \
        f'🧷Трек-код: `{track_code}`\n\n' \
        f'❤После получения заказа, будем рады увидеть ваш отзыв у нас в директ Instagram\n\n' \
        f'❗За положительный отзыв вы получите скидку 3% на следующую покупку в нашем магазине! '


def order_message(order_id: int, message: str):
    return f'Ваш заказ #{order_id} {message}'
