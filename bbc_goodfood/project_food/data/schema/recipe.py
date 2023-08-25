from typing import NamedTuple, List


class RecipeModel(NamedTuple):
    cuisine: List[str]
    types: List[str]
    name: str
    ingredients: str
    difficulty: str
    health_banners: List[str]
    instructions: str
    link: str


class RecipeParsedModel(NamedTuple):
    cuisine: List[str]
    types: List[str]
    name: str
    ingredients: str
    difficulty: str
    health_banners: List[str]
    ingredients_parsed: List[str]
    instructions: List[str]
    link: str


class ExtendedRecipeModel(RecipeModel):

    def __hash__(self):
        return hash(tuple(self.ingredients))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.ingredients == other.ingredients
