from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

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
):
    result = service_submenu.get_all_submenu(db=db, menu_id=menu_id)

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
):
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
):
    result = service_submenu.get_submenu(menu_id=menu_id, submenu_id=submenu_id, db=db)
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
):
    return service_submenu.patch_submenu(menu_id=menu_id, submenu_id=submenu_id, submenu=submenu, db=db)


@router.delete(
    path='/{menu_id}/submenus/{submenu_id}',
)
def delete_submenu(
        menu_id: str,
        submenu_id: str,
        db: Session = Depends(get_db),
):
    result = service_submenu.delete_submenu(menu_id=menu_id, submenu_id=submenu_id, db=db)
    return result
