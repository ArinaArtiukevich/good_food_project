from typing import NamedTuple, List


class RecipeModel(NamedTuple):
    cuisine: List[str]
    types: List[str]
    name: str
    ingredients: str
    difficulty: str
    health_banners: List[str]


class RecipeParsedModel(NamedTuple):
    cuisine: List[str]
    types: List[str]
    name: str
    ingredients: str
    difficulty: str
    health_banners: List[str]
    ingredients_parsed: List[str]


class ExtendedRecipeModel(RecipeModel):
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.ingredients == other.ingredients

# todo exc joblib.load not pickable?
# class RecipeParsedModel(RecipeModel):
#     def __new__(cls, cuisine, types, name, ingredients, difficulty, health_banners, ingredients_parsed):
#         return super().__new__(cls, cuisine, types, name, ingredients, difficulty, health_banners)
#
#     def __init__(self, cuisine, types, name, ingredients, difficulty, health_banners, ingredients_parsed):
#         self.ingredients_parsed = ingredients_parsed