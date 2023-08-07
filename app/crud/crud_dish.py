from uuid import uuid4

from sqlalchemy.orm import Session, aliased

from app.models.models import DishModel, SubMenuModel
from app.schemas.dishes import DishBase, DishCreate

DEL_DISH_RESULT = {'status': True, 'message': 'The dish has been deleted'}


def update_object(data: dict[str, str], obj: object, db: Session) -> None:
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)


def get_all_dish(db_submenu: SubMenuModel) -> list[DishModel]:
    return db_submenu.dish


def get_dish_by_title(
        db: Session,
        db_submenu: SubMenuModel,
        title: str,
) -> DishModel | None:
    sub = aliased(SubMenuModel)
    return (
        db.query(DishModel)
        .join(sub, DishModel.submenu)
        .filter(DishModel.title == title, sub.id == db_submenu.id)
        .first()
    )


def create_dish(
        db: Session,
        db_submenu: SubMenuModel,
        dish: DishCreate,
) -> DishModel:
    id_dish = str(uuid4())
    db_dish = DishModel(
        id=id_dish,
        submenu=db_submenu,
        title=dish.title,
        description=dish.description,
        price=dish.price,
    )
    db_dish.submenu.dishes_count += 1
    db_dish.submenu.menu.dishes_count += 1
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def get_dish_by_id(
        db: Session,
        submenu: SubMenuModel,
        dish_id: str,
) -> DishModel | None:
    db_dish = db.get(DishModel, dish_id)
    if db_dish and db_dish.submenu_id == submenu.id:
        return db_dish
    return None


def patch_dish(
        db: Session,
        db_dish: DishModel,
        dish: DishBase,
) -> DishModel:
    update_data = dish.model_dump(exclude_unset=True)
    update_object(data=update_data, obj=db_dish, db=db)
    return db_dish


def delete_dish(db: Session, db_dish: DishModel) -> dict[str, object]:
    db_dish.submenu.dishes_count -= 1
    db_dish.submenu.menu.dishes_count -= 1
    db.delete(db_dish)
    db.commit()
    return DEL_DISH_RESULT
