import pickle

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.cache.cache import delete_cache_values, r_cache
from app.crud import crud_menu, crud_submenu
from app.models.models import SubMenuModel
from app.schemas.menus import MenuCreate
from app.schemas.submenus import SubMenuCreate

MENU_NOT_FOUND = 'menu not found'
SUBMENU_NOT_FOUND = 'submenu not found'
TITLE_REGISTERED = 'Title already registered'


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


def get_all_submenu(db: Session, menu_id: str):
    if cache_data := r_cache.get(f'menu:{menu_id}:submenus'):
        return pickle.loads(cache_data)
    db_menu = get_menu_or_404(db=db, menu_id=menu_id)
    db_submenus = crud_submenu.get_all_submenu(db_menu=db_menu)
    r_cache.set(f'menu:{menu_id}:submenus', pickle.dumps(db_submenus))
    return db_submenus


def create_submenu(menu_id: str,
                   submenu: SubMenuCreate,
                   db: Session):
    db_menu = get_menu_or_404(db=db, menu_id=menu_id)
    db_submenu = crud_submenu.get_submenu_by_title(db, title=submenu.title)
    if db_submenu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TITLE_REGISTERED,
        )
    r_cache.delete(f'menu:{menu_id}:submenus')
    submenu = crud_submenu.create_submenu(db=db, db_menu=db_menu, submenu=submenu)
    return submenu


def get_submenu(menu_id: str,
                submenu_id: str,
                db: Session):
    if cache_data := r_cache.get(f'submenu:{submenu_id}'):
        return pickle.loads(cache_data)
    db_submenu = get_submenu_or_404(menu_id=menu_id, submenu_id=submenu_id, db=db)
    r_cache.set(f'submenu:{submenu_id}', pickle.dumps(db_submenu))
    r_cache.rpush(f'menu:{menu_id}:submenu.list', f'submenu:{submenu_id}')
    return db_submenu


def patch_submenu(
        menu_id: str,
        submenu_id: str,
        submenu: MenuCreate,
        db: Session
):
    db_submenu = get_submenu_or_404(menu_id=menu_id, submenu_id=submenu_id, db=db)
    r_cache.delete(f'submenu:{submenu_id}')
    r_cache.delete(f'menu:{menu_id}:submenus')
    submenu = crud_submenu.patch_submenu(db=db, db_submenu=db_submenu, submenu=submenu)
    return submenu


def delete_submenu(menu_id: str,
                   submenu_id: str,
                   db: Session):
    db_submenu = get_submenu_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        db=db,
    )
    r_cache.delete(f'submenu:{submenu_id}')
    r_cache.delete(f'menu:{menu_id}')
    r_cache.delete(f'menu:{menu_id}:submenus')
    r_cache.delete(f'submenu:{submenu_id}:dishes')
    delete_cache_values(f'submenu:{submenu_id}:dish.list', r_cache)
    r_cache.delete('menus')
    submenu = crud_submenu.delete_submenu(db_submenu=db_submenu, db=db)
    return submenu
