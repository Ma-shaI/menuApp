import pickle

from fastapi import APIRouter, Depends, status
from redis import Redis  # type: ignore[import]
from sqlalchemy.orm import Session

from app.cache.cache import get_redis
from app.dependiencies import get_db
from app.models.models import MenuModel
from app.schemas.menus import Menu, MenuCreate
from app.service import service_menu

router = APIRouter()


@router.get(
    path='/',
    response_model=list[Menu],
)
def read_menus(
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
) -> list[MenuModel]:
    if cache_data := cache.get('menus'):
        return pickle.loads(cache_data)
    result = service_menu.get_all_menu(db)
    cache.set('menus', pickle.dumps(result))
    return result


@router.post(
    path='/',
    response_model=Menu,
    status_code=status.HTTP_201_CREATED,
)
def create_menu(
        menu: MenuCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    result = service_menu.create_menu(db, menu)
    cache.delete('menus')
    return result


@router.get(
    path='/{menu_id}',
    response_model=Menu,
)
def read_menu(
        menu_id: str,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    if cache_data := cache.get(f'menu:{menu_id}'):
        return pickle.loads(cache_data)
    result = service_menu.get_menu(menu_id=menu_id, db=db)
    cache.set(f'menu:{menu_id}', pickle.dumps(result))
    return result


@router.patch(
    path='/{menu_id}',
    response_model=Menu,
)
def update_menu(
        menu_id: str,
        menu: MenuCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    db_menu = service_menu.get_menu(menu_id=menu_id, db=db)
    cache.delete(f'menu:{menu_id}')
    cache.delete('menus')
    result = service_menu.patch_menu(db=db, db_menu=db_menu, menu=menu)
    return result


@router.delete(
    path='/{menu_id}',
)
def delete_menu(
        menu_id: str,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    cache.delete('menus')
    cache.delete(f'menu:{menu_id}')
    cache.delete(f'menu:{menu_id}:submenus')
    delete_cache_values(f'menu:{menu_id}:submenu.list', cache)
    delete_cache_values(f'menu:{menu_id}:dish.list', cache)
    return service_menu.delete_menu(menu_id=menu_id, db=db)


def delete_cache_values(key_list: str, cache: Redis):
    while value := cache.rpop(key_list):
        cache.delete(value)
