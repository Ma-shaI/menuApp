from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class MenuModel(Base):
    __tablename__ = 'menus'
    id = Column(String, primary_key=True, unique=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)

    submenu = relationship(
        'SubMenuModel',
        cascade='all, delete',
        back_populates='menu',
    )


class SubMenuModel(Base):
    __tablename__ = 'submenus'
    id = Column(String, primary_key=True, unique=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    dishes_count = Column(Integer, default=0)
    menu_id = Column(String, ForeignKey('menus.id'))

    menu = relationship('MenuModel', back_populates='submenu')
    dish = relationship(
        'DishModel',
        cascade='all, delete',
        back_populates='submenu',
    )


class DishModel(Base):
    __tablename__ = 'dishes'
    id = Column(String, primary_key=True, unique=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(String, nullable=False)
    submenu_id = Column(String, ForeignKey('submenus.id'))

    submenu = relationship('SubMenuModel', back_populates='dish')
