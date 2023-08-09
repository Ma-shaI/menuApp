import pickle

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.cache.cache import r_cache
from app.crud import crud_dish, crud_menu, crud_submenu
from app.models.models import SubMenuModel
from app.schemas.dishes import DishCreate

MENU_NOT_FOUND = 'menu not found'
SUBMENU_NOT_FOUND = 'submenu not found'
TITLE_REGISTERED = 'Title already registered'
DISH_NOT_FOUND = 'dish not found'


def get_menu_or_404(menu_id: str, db: Session):
    menu = crud_menu.get_menu_by_id(menu_id=menu_id, db=db)
    if menu:
        return menu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=MENU_NOT_FOUND,
    )


def get_submenu_or_404(menu_id: str, submenu_id: str, db: Session):
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)
    db_submenu = crud_submenu.get_submenu_by_id(
        db,
        menu=db_menu,
        submenu_id=submenu_id,
    )
    if db_submenu:
        return db_submenu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=SUBMENU_NOT_FOUND,
    )


def get_submenu_or_none(
        menu_id: str,
        submenu_id: str,
        db: Session,
) -> SubMenuModel | None:
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)
    db_submenu = crud_submenu.get_submenu_by_id(
        db,
        menu=db_menu,
        submenu_id=submenu_id,
    )
    if db_submenu:
        return db_submenu
    return None


def get_dish_or_404(menu_id: str, submenu_id: str, dish_id: str, db: Session):
    db_submenu = get_submenu_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        db=db,
    )
    db_dish = crud_dish.get_dish_by_id(db=db, submenu=db_submenu, dish_id=dish_id)
    if db_dish:
        return db_dish
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=DISH_NOT_FOUND,
    )


def get_all_dish(menu_id: str,
                 submenu_id: str,
                 db: Session):
    if cache_data := r_cache.get(f'submenu:{submenu_id}:dishes'):
        return pickle.loads(cache_data)
    db_submenu = get_submenu_or_none(
        menu_id=menu_id,
        submenu_id=submenu_id,
        db=db,
    )

    if db_submenu is None:
        return []

    db_dish = crud_dish.get_all_dish(db_submenu=db_submenu)
    r_cache.set(f'submenu:{submenu_id}:dishes', pickle.dumps(db_dish))
    return db_dish


def create_dish(menu_id: str,
                submenu_id: str,
                dish: DishCreate, db: Session):
    db_submenu = get_submenu_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        db=db,
    )
    db_dishes = crud_dish.get_dish_by_title(
        db,
        db_submenu=db_submenu,
        title=dish.title,
    )
    if db_dishes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TITLE_REGISTERED,
        )
    r_cache.delete(f'submenu:{submenu_id}:dishes')
    r_cache.delete(f'submenu:{submenu_id}')
    r_cache.delete(f'menu:{menu_id}')
    db_dish = crud_dish.create_dish(db=db, db_submenu=db_submenu, dish=dish)
    return db_dish


def get_dish(menu_id: str,
             submenu_id: str,
             dish_id: str,
             db: Session):
    if cache_data := r_cache.get(f'dish:{dish_id}'):
        return pickle.loads(cache_data)
    db_dish = get_dish_or_404(menu_id=menu_id,
                              submenu_id=submenu_id,
                              dish_id=dish_id,
                              db=db, )

    r_cache.set(f'dish:{dish_id}', pickle.dumps(db_dish))
    r_cache.rpush(f'menu:{menu_id}:dish.list', f'dish:{dish_id}')
    r_cache.rpush(f'submenu:{submenu_id}:dish.list', f'dish:{dish_id}')
    return db_dish


def patch_dish(menu_id: str,
               submenu_id: str,
               dish_id: str,
               dish: DishCreate,
               db: Session):
    db_dishes = get_dish_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        db=db,
    )
    r_cache.delete(f'submenu:{submenu_id}:dishes')
    r_cache.delete(f'dish:{dish_id}')
    db_dish = crud_dish.patch_dish(db=db, db_dish=db_dishes, dish=dish)
    return db_dish


def delete_dish(menu_id: str,
                submenu_id: str,
                dish_id: str,
                db: Session):
    db_dishes = get_dish_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        db=db,
    )
    r_cache.delete(f'dish:{dish_id}')
    r_cache.delete(f'submenu:{submenu_id}:dishes')
    r_cache.delete(f'submenu:{submenu_id}')
    r_cache.delete(f'menu:{menu_id}')
    r_cache.delete('menus')
    db_dish = crud_dish.delete_dish(db=db, db_dish=db_dishes)
    return db_dish
