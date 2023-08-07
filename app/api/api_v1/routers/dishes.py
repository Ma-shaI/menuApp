import pickle

from fastapi import APIRouter, Depends, status
from redis import Redis  # type: ignore[import]
from sqlalchemy.orm import Session

from app.cache.cache import get_redis
from app.dependiencies import get_db
from app.schemas.dishes import Dish, DishCreate
from app.service import service_dish

router = APIRouter()


@router.get(
    path='/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[Dish],
    status_code=status.HTTP_200_OK,
)
def read_dishes(
        menu_id: str,
        submenu_id: str,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    if cache_data := cache.get(f'submenu:{submenu_id}:dishes'):
        return pickle.loads(cache_data)
    result = service_dish.get_all_dish(menu_id=menu_id, submenu_id=submenu_id, db=db)
    cache.set(f'submenu:{submenu_id}:dishes', pickle.dumps(result))
    return result


@router.post(
    path='/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=Dish,
    status_code=status.HTTP_201_CREATED,
)
def create_dish(
        menu_id: str,
        submenu_id: str,
        dish: DishCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    cache.delete(f'submenu:{submenu_id}:dishes')
    cache.delete(f'submenu:{submenu_id}')
    cache.delete(f'menu:{menu_id}')

    return service_dish.create_dish(menu_id=menu_id, submenu_id=submenu_id, dish=dish, db=db)


@router.get(
    path='/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Dish,
    status_code=status.HTTP_200_OK,
)
def read_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    if cache_data := cache.get(f'dish:{dish_id}'):
        return pickle.loads(cache_data)
    result = service_dish.get_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, db=db)
    cache.set(f'dish:{dish_id}', pickle.dumps(result))
    cache.rpush(f'menu:{menu_id}:dish.list', f'dish:{dish_id}')
    cache.rpush(f'submenu:{submenu_id}:dish.list', f'dish:{dish_id}')
    return result


@router.patch(
    path='/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Dish,
    status_code=status.HTTP_200_OK,
)
def update_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        dish: DishCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    cache.delete(f'submenu:{submenu_id}:dishes')
    cache.delete(f'dish:{dish_id}')
    return service_dish.patch_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, dish=dish, db=db)


@router.delete(
    path='/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    status_code=status.HTTP_200_OK,
)
def delete_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis),
):
    cache.delete(f'dish:{dish_id}')
    cache.delete(f'submenu:{submenu_id}:dishes')
    cache.delete(f'submenu:{submenu_id}')
    cache.delete(f'menu:{menu_id}')
    cache.delete('menus')
    return service_dish.delete_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, db=db)
