from pydantic import Field

from app.schemas.menus import MenuBase


class SubMenu(MenuBase):
    id: str = Field(title='id подменю')
    title: str = Field(title='Наименование подменю')
    description: str = Field(title='Описание подменю')
    dishes_count: int = Field(title='Количество блюд в подменю')

    class Config:
        from_attributes = True


class SubMenuCreate(MenuBase):
    title: str = Field(title='Наименование подменю')
    description: str = Field(title='Описание подменю')

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'Супы',
                'description': (
                    'Жидкое блюдо, в составе которого содержится '
                    'не менее 50% жидкости'
                ),
            },
        }


# response_400 = {
#     'description': 'Наименование уже существуют',
#     'content': {
#         'application/json': {
#             'example': {'detail': 'Title already registered'}
#         },
#     },
# }
# response_submenu_404 = {
#     'description': 'Подменю не найдено',
#     'content': {
#         'application/json': {'example': {'detail': 'submenu not found'}},
#     },
# }
# submenu_one = {
#     'id': 'badd3399-9c8b-47ee-8087-a236561a3ede',
#     'title': 'Супы',
#     'description': (
#         'Жидкое блюдо, в составе которого содержится ' 'не менее 50% жидкости'
#     ),
#     'dishes_count': 5,
# }
#
# submenu_two = {
#     'id': 'd93fb8d4-9460-42be-80ac-c6eb9a549e94',
#     'title': 'Блюда из мяса',
#     'description': (
#         'Это основной источник полноценных жиров, белков, '
#         'минеральных веществ и витаминов'
#     ),
#     'dishes_count': 5,
# }
#
# submenus_response_example = {
#     status.HTTP_200_OK: {
#         'description': 'Список подменю',
#         'content': {
#             'application/json': {'example': [submenu_one, submenu_two]},
#         },
#     },
# }
#
# submenu_response_example = {
#     status.HTTP_200_OK: {
#         'description': 'Конкретное подменю',
#         'content': {'application/json': {'example': submenu_one}},
#     },
#     status.HTTP_404_NOT_FOUND: response_submenu_404,
# }
#
# submenu_create_response_example = {
#     status.HTTP_201_CREATED: {
#         'description': 'Подменю создано',
#         'content': {'application/json': {'example': submenu_one}},
#     },
#     status.HTTP_400_BAD_REQUEST: response_400,
#     status.HTTP_404_NOT_FOUND: response_submenu_404,
# }
# submenu_update_response_example = {
#     status.HTTP_200_OK: {
#         'description': 'Подменю изменено',
#         'content': {'application/json': {'example': submenu_one}},
#     },
#     status.HTTP_400_BAD_REQUEST: response_400,
#     status.HTTP_404_NOT_FOUND: response_submenu_404,
# }
# submenu_delete_response_example = {
#     status.HTTP_200_OK: {
#         'description': 'Подменю удалено',
#         'content': {
#             'application/json': {
#                 'example': {
#                     'status': True,
#                     'message': 'The submenu has been deleted',
#                 },
#             },
#         },
#     },
#     status.HTTP_400_BAD_REQUEST: response_400,
#     status.HTTP_404_NOT_FOUND: response_submenu_404,
# }
