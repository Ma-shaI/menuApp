from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

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
) -> list[MenuModel]:
    result = service_menu.get_all_menu(db)
    return result


@router.post(
    path='/',
    response_model=Menu,
    status_code=status.HTTP_201_CREATED,
)
def create_menu(
        menu: MenuCreate,
        db: Session = Depends(get_db),
):
    result = service_menu.create_menu(db, menu)
    return result


@router.get(
    path='/{menu_id}',
    response_model=Menu,
)
def read_menu(
        menu_id: str,
        db: Session = Depends(get_db),
):
    result = service_menu.get_menu(menu_id=menu_id, db=db)
    return result


@router.patch(
    path='/{menu_id}',
    response_model=Menu,
)
def update_menu(
        menu_id: str,
        menu: MenuCreate,
        db: Session = Depends(get_db),
):
    result = service_menu.patch_menu(db=db, menu_id=menu_id, menu=menu)
    return result


@router.delete(
    path='/{menu_id}',
)
def delete_menu(
        menu_id: str,
        db: Session = Depends(get_db),
):
    result = service_menu.delete_menu(menu_id=menu_id, db=db)
    return result
