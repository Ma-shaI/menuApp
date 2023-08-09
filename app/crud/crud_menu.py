from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.models import MenuModel
from app.schemas.menus import MenuBase, MenuCreate

DEL_MENU_RESULT = {'status': True, 'message': 'The menu has been deleted'}


def get_all_menu(db: Session) -> list[MenuModel]:
    menus = db.query(MenuModel).all()
    return menus


def create_menu(db: Session, menu: MenuCreate) -> MenuModel:
    id_menu = str(uuid4())
    db_menu = MenuModel(
        id=id_menu,
        title=menu.title,
        description=menu.description,
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def get_menu_by_title(db: Session, title: str) -> MenuModel | None:
    return db.query(MenuModel).filter(MenuModel.title == title).first()


def get_menu_by_id(db: Session, menu_id: str) -> MenuModel | None:
    return db.get(MenuModel, menu_id)


def patch_menu(
        db: Session,
        db_menu: MenuModel,
        menu: MenuBase,
) -> MenuModel:
    update_data = menu.model_dump(exclude_unset=True)
    update_object(data=update_data, obj=db_menu, db=db)
    return db_menu


def delete_menu(db: Session, db_menu: MenuModel) -> dict[str, object]:
    db.delete(db_menu)
    db.commit()
    return DEL_MENU_RESULT


def update_object(data: dict[str, str], obj: object, db: Session) -> None:
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
