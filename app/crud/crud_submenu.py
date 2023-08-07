from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.models import MenuModel, SubMenuModel
from app.schemas.menus import MenuBase
from app.schemas.submenus import SubMenuCreate

DEL_SUBMENU_RESULT = {
    'status': True,
    'message': 'The submenu has been deleted',
}


def get_submenu_by_title(db: Session, title: str) -> SubMenuModel | None:
    return (
        db.query(SubMenuModel).filter(SubMenuModel.title == title).first()
    )


def get_submenu_by_id(
        db: Session,
        menu: MenuModel,
        submenu_id: str,
) -> SubMenuModel | None:
    db_submenu = db.get(SubMenuModel, submenu_id)
    if db_submenu and db_submenu.menu_id == menu.id:
        return db_submenu
    return None


def get_all_submenu(db_menu: MenuModel) -> list[SubMenuModel]:
    return db_menu.submenu


def create_submenu(
        db: Session,
        db_menu: MenuModel,
        submenu: SubMenuCreate,
) -> SubMenuModel:
    id_submenu = str(uuid4())
    db_submenu = SubMenuModel(
        id=id_submenu,
        menu=db_menu,
        title=submenu.title,
        description=submenu.description,
    )
    db_submenu.menu.submenus_count += 1
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def patch_submenu(
        db: Session,
        db_submenu: SubMenuModel,
        submenu: MenuBase,
) -> SubMenuModel:
    update_data = submenu.model_dump(exclude_unset=True)
    update_object(data=update_data, obj=db_submenu, db=db)
    return db_submenu


def delete_submenu(
        db: Session,
        db_submenu: SubMenuModel,
) -> dict[str, object]:
    db_submenu.menu.dishes_count -= db_submenu.dishes_count
    db_submenu.menu.submenus_count -= 1
    db.delete(db_submenu)
    db.commit()
    return DEL_SUBMENU_RESULT


def update_object(data: dict[str, str], obj: object, db: Session) -> None:
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
