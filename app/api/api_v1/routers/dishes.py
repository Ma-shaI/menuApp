from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

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
):
    result = service_dish.get_all_dish(menu_id=menu_id, submenu_id=submenu_id, db=db)
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
):
    result = service_dish.create_dish(menu_id=menu_id, submenu_id=submenu_id, dish=dish, db=db)

    return result


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
):
    result = service_dish.get_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, db=db)
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
):
    result = service_dish.patch_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, dish=dish, db=db)
    return result


@router.delete(
    path='/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    status_code=status.HTTP_200_OK,
)
def delete_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        db: Session = Depends(get_db),
):
    result = service_dish.delete_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, db=db)
    return result
