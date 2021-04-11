from collections import defaultdict
from typing import NamedTuple

from item import *


class RecipeMatch(NamedTuple):
    score: float
    diff: dict[str, float]


class Recipe:
    name: str
    ingredients: dict[str, float]

    def __init__(self, name: str):
        self.name = name
        self.ingredients = defaultdict(float)

    def get_match(self, inventory: dict[str, Item]) -> RecipeMatch:
        # with the given inventory of available items
        # check how much of the ingredients are satisfied, as score out of 100
        # e.g. 100 if all ingredients present
        # e.g. 90 if only 1 ingredient missing (leave the exact rule for you to decide)
        # e.g. 50 if multiple ingredients missing/don't have enough qty etc
        # also get the difference in ingredients
        # e.g. A, -2 if ingredient A is missing by 2 units in inventory
        # e.g. B, 0 if there is exact amount needed for B
        # e.g. C, 3 if have 3 units more than needed
        # return the values like below
        diff = {"A": -2, "B": 0, "C": 3}
        return RecipeMatch(12.3, diff)


class Recipes:
    recipes: dict[str, Recipe]

    def __init__(self):
        self.recipes = {}
        self.__load_recipes()

    def __load_recipes(self):
        # read and parse recipes from a file, or multiple files (or whatever you decide)
        # populate Recipe object with real values like below
        recipe = Recipe("name of my recipe")
        recipe.ingredients["ingredient 1"] = 3
        recipe.ingredients["ingredient 2"] = 1
        self.recipes[recipe.name] = recipe

    def get_best_recipes(self, n: int, inventory: dict[str, Item]) -> dict[str, float]:
        # with the given inventory, get the top n (highest score) recipes
        # return as a dict of name and score
        best = {"rec1": 100, "rec2": 100, "rec3": 85.56789}
        return best

    def view_recipe(self, name: str, inventory: dict[str, Item]) -> list[str]:
        # find the recipe if exists, and list out the ingredients needed, and corresponding qty in current inventory
        lines = ["my recipe name",
                 f"{'Ingredient':<20}{'Needed':>10}{'Have':>10}"]
        return lines
