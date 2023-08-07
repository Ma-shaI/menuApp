from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_menu
from app.models.models import MenuModel
from app.schemas.menus import MenuBase, MenuCreate

MENU_NOT_FOUND = 'menu not found'
TITLE_REGISTERED = 'Title already registered'


def get_all_menu(db: Session):
    db_menus = crud_menu.get_all_menu(db)
    return db_menus


def create_menu(db: Session, menu: MenuCreate):
    db_menu = crud_menu.get_menu_by_title(db, title=menu.title)
    if db_menu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TITLE_REGISTERED,
        )
    return crud_menu.create_menu(db=db, menu=menu)


def get_menu(menu_id: str, db: Session):
    db_menu = crud_menu.get_menu_by_id(menu_id=menu_id, db=db)
    if db_menu:
        return db_menu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=MENU_NOT_FOUND,
    )


def patch_menu(db: Session,
               db_menu: MenuModel,
               menu: MenuBase, ) -> dict[str, object]:
    db_menu = crud_menu.patch_menu(db=db, db_menu=db_menu, menu=menu)
    return db_menu


def delete_menu(db: Session, menu_id: str):
    db_menus = get_menu(menu_id=menu_id, db=db)
    db_menu = crud_menu.delete_menu(db=db, db_menu=db_menus)
    return db_menu
