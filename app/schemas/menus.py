import warnings

from pydantic import BaseModel, Field

warnings.filterwarnings('ignore', category=DeprecationWarning)


class MenuBase(BaseModel):
    title: str | None = Field(title='Наименование')
    description: str | None = Field(title='Описание')


class MenuCreate(MenuBase):
    title: str = Field(title='Наименование меню')
    description: str = Field(title='Описание меню')

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'Горячие блюда',
                'description': 'Основное составляющее обеденного стола',
            },
        }


class Menu(MenuBase):
    id: str = Field(title='id меню')
    title: str = Field(title='Наименование меню')
    description: str = Field(title='Описание меню')
    submenus_count: int = Field(title='Количество подменю в меню')
    dishes_count: int = Field(title='Количество блюд в меню')

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
# response_menu_404 = {
#     'description': 'Меню не найдено',
#     'content': {'application/json': {'example': {'detail': 'menu not found'}}},
# }
# menu_one = {
#     'id': '4d6723c7-3e4b-427c-b116-66904a86eef5',
#     'title': 'Горячие блюда',
#     'description': 'Основное составляющее обеденного стола',
#     'submenus_count': 3,
#     'dishes_count': 12,
# }
# menu_two = {
#     'id': '3ffdfed1-e6c7-4066-b5b4-9dad0cffea22',
#     'title': 'Холодные закуски',
#     'description': (
#         'Небольшое по объёму преимущественно холодное ' 'блюдо первой подачи'
#     ),
#     'submenus_count': 5,
#     'dishes_count': 21,
# }
# enus_response_example = {
#     status.HTTP_200_OK: {
#         'description': 'Список меню',
#         'content': {'application/json': {'example': [menu_one, menu_two]}},
#     },
# }
#
# menu_response_example = {
#     status.HTTP_200_OK: {
#         'description': 'Конкретное меню',
#         'content': {'application/json': {'example': menu_one}},
#     },
#     status.HTTP_404_NOT_FOUND: response_menu_404,
# }
#
# menu_create_response_example = {
#     status.HTTP_201_CREATED: {
#         'description': 'Меню создано',
#         'content': {'application/json': {'example': menu_one}},
#     },
#     status.HTTP_400_BAD_REQUEST: response_400,
# }
# menu_update_response_example = {
#     status.HTTP_200_OK: {
#         'description': 'Меню изменено',
#         'content': {'application/json': {'example': menu_one}},
#     },
#     status.HTTP_400_BAD_REQUEST: response_400,
#     status.HTTP_404_NOT_FOUND: response_menu_404,
# }
# menu_delete_response_example = {
#     status.HTTP_200_OK: {
#         'description': 'Меню удалено',
#         'content': {
#             'application/json': {
#                 'example': {
#                     'status': True,
#                     'message': 'The menu has been deleted',
#                 },
#             },
#         },
#     },
#     status.HTTP_404_NOT_FOUND: response_menu_404,
# }
