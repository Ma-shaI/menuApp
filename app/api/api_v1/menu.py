from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db, Base, engine

MENU_NOT_FOUND = "menu not found"
SUBMENU_NOT_FOUND = "submenu not found"
DISH_NOT_FOUND = "dish not found"
TITLE_REGISTERED = "Title already registered"
Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.get(
    path="/",
    response_model=list[schemas.Menu],
    status_code=status.HTTP_200_OK,
)
def read_menus(
        db: Session = Depends(get_db),

):
    result = crud.get_all_menu(db=db)
    return result


@router.post(
    path="/",
    response_model=schemas.Menu,
    status_code=status.HTTP_201_CREATED,
)
def create_menu(
        menu: schemas.MenuCreate,
        db: Session = Depends(get_db),

):
    db_menu = crud.get_menu_by_title(db, title=menu.title)
    if db_menu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TITLE_REGISTERED,
        )

    return crud.create_menu(db=db, menu=menu)


@router.get(
    path="/{menu_id}",
    response_model=schemas.Menu,
    status_code=status.HTTP_200_OK,
)
def read_menu(
        menu_id: str,
        db: Session = Depends(get_db),

):
    result = get_menu_or_404(menu_id=menu_id, db=db)
    if not result:
        return []
    return result


@router.patch(
    path="/{menu_id}",
    response_model=schemas.Menu,
    status_code=status.HTTP_200_OK,
)
def update_menu(
        menu_id: str,
        menu: schemas.MenuCreate,
        db: Session = Depends(get_db),

):
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)

    return crud.patch_menu(db=db, db_menu=db_menu, menu=menu)


@router.delete(
    path="/{menu_id}",
    status_code=status.HTTP_200_OK,
)
def delete_menu(
        menu_id: str,
        db: Session = Depends(get_db),

):
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)

    return crud.delete_menu(db_menu=db_menu, db=db)


@router.get(
    path="/{menu_id}/submenus",
    response_model=list[schemas.SubMenu],
    status_code=status.HTTP_200_OK,
)
def read_submenus(
        menu_id: str,
        db: Session = Depends(get_db),

):
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)
    result = crud.get_all_submenu(db_menu=db_menu)

    return result


@router.post(
    path="/{menu_id}/submenus",
    response_model=schemas.SubMenu,
    status_code=status.HTTP_201_CREATED,
)
def create_submenu(
        menu_id: str,
        submenu: schemas.SubMenuCreate,
        db: Session = Depends(get_db),

):
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)
    db_submenu = crud.get_submenu_by_title(db, title=submenu.title)
    if db_submenu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TITLE_REGISTERED,
        )

    return crud.create_submenu(db=db, db_menu=db_menu, submenu=submenu)


@router.get(
    path="/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubMenu,
    status_code=status.HTTP_200_OK,
)
def read_submenu(
        menu_id: str,
        submenu_id: str,
        db: Session = Depends(get_db),

):
    result = get_submenu_or_404(menu_id=menu_id, submenu_id=submenu_id, db=db)

    return result


@router.patch(
    path="/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubMenu,
    status_code=status.HTTP_200_OK,
)
def update_submenu(
        menu_id: str,
        submenu_id: str,
        submenu: schemas.MenuCreate,
        db: Session = Depends(get_db),

):
    db_submenu = get_submenu_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        db=db,
    )

    return crud.patch_submenu(db=db, db_submenu=db_submenu, submenu=submenu)


@router.delete(
    path="/{menu_id}/submenus/{submenu_id}",
    status_code=status.HTTP_200_OK,
)
def delete_submenu(
        menu_id: str,
        submenu_id: str,
        db: Session = Depends(get_db),

):
    db_submenu = get_submenu_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        db=db,
    )

    return crud.delete_submenu(db_submenu=db_submenu, db=db)


@router.get(
    path="/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=list[schemas.Dish],
    status_code=status.HTTP_200_OK,
)
def read_dishes(
        menu_id: str,
        submenu_id: str,
        db: Session = Depends(get_db),

):
    db_submenu = get_submenu_or_none(
        menu_id=menu_id,
        submenu_id=submenu_id,
        db=db,
    )
    if db_submenu is None:
        return []
    result = crud.get_all_dish(db_submenu=db_submenu)

    return result


@router.post(
    path="/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=schemas.Dish,
    status_code=status.HTTP_201_CREATED,
)
def create_dish(
        menu_id: str,
        submenu_id: str,
        dish: schemas.DishCreate,
        db: Session = Depends(get_db),

):
    db_submenu = get_submenu_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        db=db,
    )
    db_dish = crud.get_dish_by_title(
        db,
        db_submenu=db_submenu,
        title=dish.title,
    )
    if db_dish:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TITLE_REGISTERED,
        )

    return crud.create_dish(db=db, db_submenu=db_submenu, dish=dish)


@router.get(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.Dish,
    status_code=status.HTTP_200_OK,
)
def read_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        db: Session = Depends(get_db),

):
    result = get_dish_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        db=db,
    )

    return result


@router.patch(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.Dish,
    status_code=status.HTTP_200_OK,
)
def update_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        dish: schemas.DishCreate,
        db: Session = Depends(get_db),

):
    db_dish = get_dish_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        db=db,
    )

    return crud.patch_dish(db=db, db_dish=db_dish, dish=dish)


@router.delete(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    status_code=status.HTTP_200_OK,
)
def delete_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        db: Session = Depends(get_db),

):
    db_dish = get_dish_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        db=db,
    )

    return crud.delete_dish(db_dish=db_dish, db=db)


def get_menu_or_404(menu_id: str, db: Session):
    menu = crud.get_menu_by_id(menu_id=menu_id, db=db)
    if menu:
        return menu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=MENU_NOT_FOUND,
    )


def get_submenu_or_404(menu_id: str, submenu_id: str, db: Session):
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)
    db_submenu = crud.get_submenu_by_id(
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
) -> models.SubMenu | None:
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)
    db_submenu = crud.get_submenu_by_id(
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
    db_dish = crud.get_dish_by_id(db=db, submenu=db_submenu, dish_id=dish_id)
    if db_dish:
        return db_dish
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=DISH_NOT_FOUND,
    )
