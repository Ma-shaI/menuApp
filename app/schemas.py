from fastapi import status
from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    title: str | None = Field()
    description: str | None = Field()


class MenuCreate(MenuBase):
    title: str = Field()
    description: str = Field()


class Menu(MenuBase):
    id: str = Field()
    title: str = Field()
    description: str = Field()
    submenus_count: int = Field()
    dishes_count: int = Field()

    class Config:
        from_attributes = True


class SubMenu(MenuBase):
    id: str = Field()
    title: str = Field()
    description: str = Field()
    dishes_count: int = Field()

    class Config:
        from_attributes = True


class SubMenuCreate(MenuBase):
    title: str = Field()
    description: str = Field()


class DishBase(BaseModel):
    title: str | None
    description: str | None
    price: str | None


class DishCreate(DishBase):
    title: str = Field()
    description: str = Field()
    price: str = Field()


class Dish(DishBase):
    id: str = Field()
    title: str = Field()
    description: str = Field()
    price: str = Field()

    class Config:
       from_attributes = True
