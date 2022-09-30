from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine("sqlite:///factory.db")
Base = declarative_base()


class Process(Base):
    """
    Sukuria Process DB lentelę
    """

    __tablename__ = "Processes"
    id = Column(Integer, primary_key=True)
    name = Column("Process", String)
    produced_material = Column("Produced material", Integer, ForeignKey("Materials.id"))
    efficiency = Column("Efficiency", Float)
    materials = relationship("Materials")

    def __init__(self, name, produced_material, efficiency):
        self.name = name
        self.produced_material = produced_material
        self.efficiency = efficiency

    def __repr__(self):
        return f"{self.id}. {self.name} - {self.produced_material} - {self.efficiency} kg/h"


class Recipe(Base):
    """
    Sukuria Recipe DB lentelę
    """

    __tablename__ = "Recipies"
    id = Column(Integer, primary_key=True)
    name = Column("Recipe", String)
    material1 = Column("Material_1", Float)
    material2 = Column("Material_2", Float)
    material3 = Column("Material_3", Float)
    material4 = Column("Material_4", Float)
    material5 = Column("Material_5", Float)

    def __init__(self, name, material1, material2, material3, material4, material5):
        self.name = name
        self.material1 = material1
        self.material2 = material2
        self.material3 = material3
        self.material4 = material4
        self.material5 = material5

    def __repr__(self):
        return (
            f"{self.id}. {self.name} - {self.material1} ; {self.material2} ; "
            f"{self.material3} ; {self.material4} ; {self.material5}"
        )


class Storage(Base):
    """
    Sukuria Storage DB lentelę
    """

    __tablename__ = "Storage"
    id = Column(Integer, primary_key=True)
    name = Column("Raw Material", Integer, ForeignKey("Materials.id"))
    amount = Column("Amount", Float)
    materials = relationship("Materials")

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def __repr__(self):
        return f"{self.id}. {self.name} - {self.amount} kg"


class Materials(Base):
    """
    Sukuria Materials DB lentelę
    """

    __tablename__ = "Materials"
    id = Column(Integer, primary_key=True)
    name = Column("Material", String)
    price = Column("Price", Float)

    def __init__(self, name, price):
        self.name = name
        self.amount = price

    def __repr__(self):
        return f"{self.id}. {self.name} - {self.price}"


class Orders(Base):
    """
    Sukuria Orders DB lentelę
    """

    __tablename__ = "Orders"
    id = Column(Integer, primary_key=True)
    date = Column("Date", String)
    recipe = Column("Recipe", Integer, ForeignKey("Recipies.id"))
    amount = Column("Amount", Float)
    man_cost = Column("Manufacturing cost", Float)
    sell_price = Column("Selling price", Float)
    recipe_info = relationship("Recipe")

    def __init__(self, date, recipe, amount, man_cost, sell_price):
        self.date = date
        self.name = date
        self.recipe = recipe
        self.amount = amount
        self.man_cost = man_cost
        self.sell_price = sell_price

    def __repr__(self):
        return f"{self.id}. {self.date} - {self.recipe_info.name} Amount: {self.amount}kg " \
               f"Manufacturing cost: {self.man_cost} Selling price: {self.sell_price}"


Base.metadata.create_all(engine)
