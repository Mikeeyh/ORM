from typing import List

from sqlalchemy.orm import sessionmaker

from helpers import session_decorator
from models import engine, Recipe, Chef

Session = sessionmaker(bind=engine)
session = Session()


@session_decorator(session)
def create_recipe(name: str, ingredients: str, instructions: str) -> None:
    new_recipe = Recipe(
        name=name,
        ingredients=ingredients,
        instructions=instructions
    )

    session.add(new_recipe)


recipes = [
    ("Spaghetti Carbonara", "Pasta, Eggs, Pancetta, Cheese", "Cook the pasta, mix it with eggs, pancetta, and cheese"),
    ("Chicken Stir-Fry", "Chicken, Bell Peppers, Soy Sauce, Vegetables", "Stir-fry chicken and vegetables with soy sauce"),
    ("Caesar Salad", "Romaine Lettuce, Croutons, Caesar Dressing", "Toss lettuce with dressing and top with croutons")
]

# for name, ingredients, instructions in recipes:
#     create_recipe(name, ingredients, instructions)


# recipes_in_db = session.query(Recipe).all()
# for recipe in recipes_in_db:
#     print(f"Recipe name: {recipe.name}")


@session_decorator(session)
def update_recipe_by_name(name: str, new_name: str, new_ingredients: str, new_instructions: str) -> int:
    records_changed: int = (
        session.query(Recipe)
        .filter_by(name=name)
        .update({
            Recipe.name: new_name,
            Recipe.ingredients: new_ingredients,
            Recipe.instructions: new_instructions
        })
    )

    """OR:"""

    # recipe_to_update = session.query(Recipe).filter_by(name=name).first()
    #
    # recipe_to_update.name = new_name
    # recipe_to_update.ingredients = new_ingredients
    # recipe_to_update.instructions = new_instructions

    # return recipe_to_update

    return records_changed


# update_recipe_by_name(
#     "Caesar Salad",
#     "Salad Caesar",
#     "Romaine Lettuce, Croutons, Caesar Dressing",
#     "Toss lettuce with dressing and top with croutons"
# )


@session_decorator(session)
def delete_recipe_by_name(name: str) -> int:
    records_changed: int = (
        session.query(Recipe)
        .filter_by(name=name)  # we use 'filter_by' when we have something that can be directly filtered ( name = name )
        .delete()
    )

    return records_changed


# delete_recipe_by_name("Salad Caesar")


@session_decorator(session, autoclose_session=False)
def get_recipes_by_ingredient(ingredient_name: str) -> List:
    recipes_with_ingredient = (
        session.query(Recipe)
        .filter(Recipe.ingredients.ilike(f"%{ingredient_name}%"))
        .all()
    )

    return recipes_with_ingredient


# print(get_recipes_by_ingredient("Cheese")[0].name)
# Adding autoclose_session because we need open session in order to take the name of the recipe,
# and we close manually the session after that
# session.close()


@session_decorator(session)
def swap_recipe_ingredients_by_name(first_recipe_name: str, second_recipe_name: str):
    first_recipe = (
        session.query(Recipe)
        .filter_by(name=first_recipe_name)
        .with_for_update()
        .one()
    )

    second_recipe = (
        session.query(Recipe)
        .filter_by(name=second_recipe_name)
        .with_for_update()  # locking the record so no other session can update it till the end of the current session
        .one()  # if there isn't any record found -> returns an error, if more than 1 record found -> returns an error
    )

    first_recipe.ingredients, second_recipe.ingredients = second_recipe.ingredients, first_recipe.ingredients


# swap_recipe_ingredients_by_name("Spaghetti Carbonara", "Chicken Stir-Fry")


@session_decorator(session)
def relate_recipe_with_chef_by_name(recipe_name: str, chef_name: str):
    recipe = session.query(Recipe).filter_by(name=recipe_name).first()

    if recipe and recipe.chef:
        raise Exception(f"Recipe: {recipe_name} already has a related chef")

    chef = session.query(Chef).filter_by(name=chef_name).first()
    recipe.chef = chef

    return f"Related recipe {recipe_name} with chef {chef_name}"


# print(relate_recipe_with_chef_by_name("Spaghetti Carbonara", "Mike"))


@session_decorator(session)
def get_recipes_with_chef():
    result = []
    all_recipes = session.query(Recipe).all()
    for recipe in all_recipes:
        if recipe.chef:
            result.append(f"Recipe: {recipe.name} made by chef: {recipe.chef.name if recipe.chef else "None"} ")

    return '\n'.join(result)

    """Second way"""
    # recipes_with_chef = (
    #     session.query(Recipe.name, Chef.name.label("chef_name"))  # label is alais, but it is not needed here
    #     .join(Chef, Recipe.chef)
    #     .all()
    # )
    #
    # return '\n'.join(
    #     f"Recipe: {recipe_name} made by chef: {chef_name}"
    #     for recipe_name, chef_name in recipes_with_chef
    # )


print(get_recipes_with_chef())

