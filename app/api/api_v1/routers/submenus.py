import pickle

from fastapi import APIRouter, Depends, status
from redis import Redis  # type: ignore[import]
from sqlalchemy.orm import Session

from app.cache.cache import get_redis
from app.dependiencies import get_db
from app.schemas.menus import MenuCreate
from app.schemas.submenus import SubMenu, SubMenuCreate
from app.service import service_submenu

router = APIRouter()


@router.get(
    path='/{menu_id}/submenus',
    response_model=list[SubMenu],

)
def read_submenus(
        menu_id: str,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    if cache_data := cache.get(f'menu:{menu_id}:submenus'):
        return pickle.loads(cache_data)

    result = service_submenu.get_all_submenu(db=db, menu_id=menu_id)
    cache.set(f'menu:{menu_id}:submenus', pickle.dumps(result))
    return result


@router.post(
    path='/{menu_id}/submenus',
    response_model=SubMenu,
    status_code=status.HTTP_201_CREATED,
)
def create_submenu(
        menu_id: str,
        submenu: SubMenuCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    cache.delete(f'menu:{menu_id}:submenus')
    result = service_submenu.create_submenu(menu_id=menu_id, submenu=submenu, db=db)
    return result


@router.get(
    path='/{menu_id}/submenus/{submenu_id}',
    response_model=SubMenu,
)
def read_submenu(
        menu_id: str,
        submenu_id: str,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    if cache_data := cache.get(f'submenu:{submenu_id}'):
        return pickle.loads(cache_data)
    result = service_submenu.get_submenu(menu_id=menu_id, submenu_id=submenu_id, db=db)
    cache.set(f'submenu:{submenu_id}', pickle.dumps(result))
    cache.rpush(f'menu:{menu_id}:submenu.list', f'submenu:{submenu_id}')
    return result


@router.patch(
    path='/{menu_id}/submenus/{submenu_id}',
    response_model=SubMenu,
)
def update_submenu(
        menu_id: str,
        submenu_id: str,
        submenu: MenuCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    cache.delete(f'submenu:{submenu_id}')
    cache.delete(f'menu:{menu_id}:submenus')
    return service_submenu.patch_submenu(menu_id=menu_id, submenu_id=submenu_id, submenu=submenu, db=db)


@router.delete(
    path='/{menu_id}/submenus/{submenu_id}',
)
def delete_submenu(
        menu_id: str,
        submenu_id: str,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    cache.delete(f'submenu:{submenu_id}')
    cache.delete(f'menu:{menu_id}')
    cache.delete(f'menu:{menu_id}:submenus')
    cache.delete(f'submenu:{submenu_id}:dishes')

    delete_cache_values(f'submenu:{submenu_id}:dish.list', cache)
    cache.delete('menus')
    return service_submenu.delete_submenu(menu_id=menu_id, submenu_id=submenu_id, db=db)


def delete_cache_values(key_list: str, cache: Redis):
    while value := cache.rpop(key_list):
        cache.delete(value)
