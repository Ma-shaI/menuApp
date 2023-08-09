import pickle

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.cache.cache import delete_cache_values, r_cache
from app.crud import crud_menu
from app.schemas.menus import MenuBase, MenuCreate

MENU_NOT_FOUND = 'menu not found'
TITLE_REGISTERED = 'Title already registered'


def get_menu_or_404(menu_id: str, db: Session):
    menu = crud_menu.get_menu_by_id(menu_id=menu_id, db=db)
    if menu:
        return menu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=MENU_NOT_FOUND,
    )


def get_all_menu(db: Session):
    if cache_data := r_cache.get('menus'):
        return pickle.loads(cache_data)
    db_menus = crud_menu.get_all_menu(db)
    r_cache.set('menus', pickle.dumps(db_menus))
    return db_menus


def create_menu(db: Session, menu: MenuCreate):
    db_menu = crud_menu.get_menu_by_title(db, title=menu.title)
    if db_menu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TITLE_REGISTERED,
        )
    r_cache.delete('menus')
    return crud_menu.create_menu(db=db, menu=menu)


def get_menu(menu_id: str, db: Session):
    if cache_data := r_cache.get(f'menu:{menu_id}'):
        return pickle.loads(cache_data)
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)
    r_cache.set(f'menu:{menu_id}', pickle.dumps(db_menu))
    return db_menu


def patch_menu(db: Session,
               menu_id: str,
               menu: MenuBase, ) -> dict[str, object]:
    r_cache.delete(f'menu:{menu_id}')
    r_cache.delete('menus')
    db_menus = get_menu_or_404(menu_id=menu_id, db=db)
    db_menu = crud_menu.patch_menu(db=db, db_menu=db_menus, menu=menu)
    return db_menu


def delete_menu(db: Session, menu_id: str):
    r_cache.delete('menus')
    r_cache.delete(f'menu:{menu_id}:submenus')
    r_cache.delete(f'menu:{menu_id}')
    delete_cache_values(f'menu:{menu_id}:submenu.list', r_cache)
    delete_cache_values(f'menu:{menu_id}:dish.list', r_cache)
    db_menus = get_menu_or_404(menu_id=menu_id, db=db)
    db_menu = crud_menu.delete_menu(db=db, db_menu=db_menus)
    return db_menu
