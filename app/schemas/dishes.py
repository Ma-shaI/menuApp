from pydantic import BaseModel, Field


class DishBase(BaseModel):
    title: str | None
    description: str | None
    price: str | None


class DishCreate(DishBase):
    title: str = Field(title='Наименование блюда')
    description: str = Field(title='Описание блюда')
    price: str = Field(title='Стоимость блюда')

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'Суп харчо',
                'description': 'Суп из говядины с рисом и кислым соусом.',
                'price': '152.50',
            },
        }


class Dish(DishBase):
    id: str = Field(title='id блюда')
    title: str = Field(title='Наименование блюда')
    description: str = Field(title='Описание блюда')
    price: str = Field(title='Стоимость блюда')

    class Config:
        from_attributes = True

# response_400 = {
#     'description': 'Наименование уже существуют',
#     'content': {
#         'application/json': {
#             'example': {'detail': 'Title already registered'}
#         },
#     },
# }
#
# response_dish_404 = {
#     'description': 'Блюдо не найдено',
#     'content': {'application/json': {'example': {'detail': 'dish not found'}}},
# }
#
# dish_one = {
#     'id': '96ec8ff8-1def-4312-8756-7fbec1dc04b1',
#     'title': 'Суп харчо',
#     'description': 'Суп из говядины с рисом и кислым соусом.',
#     'price': '152.50',
# }
# dish_two = {
#     'id': '147d484c-1239-4354-a711-a363efc8f45a',
#     'title': 'Суп харчо',
#     'description': (
#         'Мясной фарш из рубленной баранины, нанизанный на шампур '
#         'и зажаренный на мангале.'
#     ),
#     'price': '280.32',
# }
# dishes_response_example = {
#     status.HTTP_200_OK: {
#         'description': 'Список блюд',
#         'content': {'application/json': {'example': [dish_one, dish_two]}},
#     },
# }
#
# dish_response_example = {
#     status.HTTP_200_OK: {
#         'description': 'Конкретное блюдо',
#         'content': {'application/json': {'example': dish_one}},
#     },
#     status.HTTP_404_NOT_FOUND: response_dish_404,
# }
#
# dish_create_response_example = {
#     status.HTTP_201_CREATED: {
#         'description': 'Блюдо создано',
#         'content': {'application/json': {'example': dish_one}},
#     },
#     status.HTTP_400_BAD_REQUEST: response_400,
#     status.HTTP_404_NOT_FOUND: response_dish_404,
# }
# dish_update_response_example = {
#     status.HTTP_200_OK: {
#         'description': 'Блюдо изменено',
#         'content': {'application/json': {'example': dish_one}},
#     },
#     status.HTTP_400_BAD_REQUEST: response_400,
#     status.HTTP_404_NOT_FOUND: response_dish_404,
# }
# dish_delete_response_example = {
#     status.HTTP_200_OK: {
#         'description': 'Блюдо удалено',
#         'content': {
#             'application/json': {
#                 'example': {
#                     'status': True,
#                     'message': 'The dish has been deleted',
#                 },
#             },
#         },
#     },
#     status.HTTP_400_BAD_REQUEST: response_400,
#     status.HTTP_404_NOT_FOUND: response_dish_404, }
