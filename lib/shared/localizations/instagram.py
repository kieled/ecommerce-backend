from shared.schemas import DescriptionSchema


def description(data: DescriptionSchema):
    materials = '\n'.join(map(lambda x: f"{x['name']}: {x['value']}", data.materials))
    return f'{data.title}\n' \
           f'Price: {data.price}$\n\n' \
           f'Курсы валют в посте указаны на момент ' \
           f'публикации, актуальные курсы вы можете узнать на нашем сайте!\n' \
           f'—————————————————————\n' \
           f'{data.description}\n' \
           f'—————————————————————\n' \
           f'ID: {data.id}\n' \
           f'{materials}' \
           f'Sizes: {" / ".join(data.sizes)}\n' \
           f'—————————————————————\n' \
           f'🛒 Для заказа заходите к нам на сайт, ссылка в описании профиля!\n' \
           f'⚡ По вопросам пишите в DM (директ)'
