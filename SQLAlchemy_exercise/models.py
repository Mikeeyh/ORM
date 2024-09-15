from sqlalchemy import Column, Integer, String, Text, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

CONNECTION_STRING = 'postgresql+psycopg2://postgres-user:password@localhost:5432/sql_alchemy_exercise'

engine = create_engine(CONNECTION_STRING)
Base = declarative_base()


class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)

    chef_id = Column(
        Integer,
        ForeignKey('chefs.id')
    )

    chef = relationship(
        "Chef",
        back_populates="recipes"
    )


class Chef(Base):
    __tablename__ = 'chefs'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    recipes = relationship(
        "Recipe",
        back_populates="chef"
    )
