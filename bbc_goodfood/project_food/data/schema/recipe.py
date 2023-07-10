from typing import NamedTuple, List


class RecipeModel(NamedTuple):
    cuisine: List[str]
    types: List[str]
    name: str
    ingredients: List[str]
    difficulty: str
    health_banners: List[str]


class RecipeParsedModel(RecipeModel):
    ingredients_parsed: List[str]
