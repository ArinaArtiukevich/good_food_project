import ast

import pandas as pd
import re
import nltk

from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
# todo delete SnowballStemmer - более "сильный"
from typing import List
from constants import DATA_CSV_PATH_SHORT, DATA_PARSED_CSV_PATH, DATA_CSV_PATH_FULL, INGREDIENTS_COLUMN, \
    INGREDIENTS_PARSED_COLUMN, DROP_DUPLICATES_BY_COLUMN


class DataPreprocessing:
    MEASURES = ['cup', 'tsp', 'tbsp', 'c', 'fl oz', 'pt', 'qt', 'gal', 'g', 'kg', 'mg', 'oz', 'lb', 'slice', 'piece',
                'pinch', 'dash', 'whole', 'dozen', 'count', 'pkg', 'can', 'jar', 'carton', 'stick', 'drop', 'cm', 'm',
                'ml', 'l', 'x', 'pint', 'cubes', 'cube', 'pack']
    # STOP_WORDS = ['a', 'an', 'the', 'in', 'on', 'at', 'for', 'of', 'with', 'to', 'from', 'by', 'as', 'is', 'are',
    # 'was', 'were', 'has', 'have', 'had', 'need']
    STOP_WORDS = set(nltk.corpus.stopwords.words('english') + ['new', "%"])
    PATTERN_REMOVE_DIGITS_BRACKETS = r'(\d|\½|¼)(\-?\.?)\s?|\((.*?)\)|\\u|\\|\/'
    PATTERN_JOIN_WORDS = r'\b(?:{})\s?\b'
    PATTERN_SPLIT_WORDS = r'\W+|\s+'

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = SnowballStemmer("english")

    def create_pattern(self, join_pattern: str, words: List[str]) -> str:
        return join_pattern.format('|'.join(words))

    # TODO join prettify_string_ingredients and prettify_df_ingredients ???
    def prettify_string_ingredients(self, input_string: str) -> List[str]:
        modified_string = input_string
        # lower case
        modified_string = modified_string.lower()

        # remove numbers + "("..")" + u2028
        modified_string = re.sub(self.PATTERN_REMOVE_DIGITS_BRACKETS, "", modified_string)

        # measures
        modified_string = re.sub(self.create_pattern(self.PATTERN_JOIN_WORDS, self.MEASURES), "", modified_string)

        # stop_words
        modified_string = re.sub(self.create_pattern(self.PATTERN_JOIN_WORDS, list(self.STOP_WORDS)), "",
                                 modified_string)
        # create List
        ingredients_list = ast.literal_eval(modified_string)

        # remove comas and multiple spaces
        ingredients_list = list(map(self.preprocess_ingredient, ingredients_list))
        return ingredients_list

    def prettify_df_ingredients(self, df_recipes: pd.DataFrame) -> pd.DataFrame:
        df_copy = df_recipes.copy()
        # df["ingredients"] - str

        # lower case
        df_copy[INGREDIENTS_PARSED_COLUMN] = df_copy[INGREDIENTS_COLUMN].str.lower()

        # remove numbers + "("..")" + u2028
        df_copy[INGREDIENTS_PARSED_COLUMN] = df_copy[INGREDIENTS_PARSED_COLUMN].str.replace(self.PATTERN_REMOVE_DIGITS_BRACKETS, "", regex=True)

        # measures
        pattern = self.create_pattern(self.PATTERN_JOIN_WORDS, self.MEASURES)
        df_copy[INGREDIENTS_PARSED_COLUMN] = df_copy[INGREDIENTS_PARSED_COLUMN].str.replace(pattern, "", regex=True)

        # stop_words
        pattern = self.create_pattern(self.PATTERN_JOIN_WORDS, list(self.STOP_WORDS))
        df_copy[INGREDIENTS_PARSED_COLUMN] = df_copy[INGREDIENTS_PARSED_COLUMN].str.replace(pattern, "", regex=True)

        # create list from string
        df_copy[INGREDIENTS_PARSED_COLUMN] = df_copy[INGREDIENTS_PARSED_COLUMN].apply(ast.literal_eval).tolist()

        # TODO DEL
        # df_copy[INGREDIENTS_COLUMN] = df_copy[INGREDIENTS_COLUMN].apply(lambda ingredients_string: ingredients_string.translate(str.maketrans({"\'": '\"', '\"': "\'"})))
        # df_copy[INGREDIENTS_COLUMN] = df_copy[INGREDIENTS_COLUMN].apply(lambda ingredients_string: json.loads(str(ingredients_string)))

        # remove comas and multiple spaces
        df_copy[INGREDIENTS_PARSED_COLUMN] = df_copy[INGREDIENTS_PARSED_COLUMN].apply(
            lambda ingredients: [self.preprocess_ingredient(ingredient) for ingredient in ingredients])

        return df_copy

    def preprocess_ingredient(self, ingredient: str) -> str:
        ingredient = ingredient.replace(",", "")
        ingredient = " ".join(ingredient.split())
        return ingredient

    def preprocess_list_ingredients(self, list_ingredients: List) -> List:
        result = []
        for ingredients in list_ingredients:
            words = re.split(self.PATTERN_SPLIT_WORDS, ingredients)
            words = [self.lemmatizer.lemmatize(word) for word in words]
            words = [self.stemmer.stem(word) for word in words]
            if words:
                result.append(' '.join(words))
        return result

    def preprocess_request(self, req: str) -> List:
        ingredients_list = self.prettify_string_ingredients(req)
        return self.preprocess_list_ingredients(ingredients_list)

    def preprocess_df(self, df_recipes: pd.DataFrame) -> pd.DataFrame:
        result_df = df_recipes.copy()
        result_df = self.prettify_df_ingredients(result_df)
        result_df[INGREDIENTS_PARSED_COLUMN] = result_df[INGREDIENTS_PARSED_COLUMN].apply(lambda x: self.preprocess_list_ingredients(x))
        return result_df

if __name__ == "__main__":
    df = pd.read_csv(DATA_CSV_PATH_SHORT, sep='\t')
    recipe_df = df.copy()
    print(recipe_df.shape)
    recipe_df.sort_values(DROP_DUPLICATES_BY_COLUMN, inplace=True)
    recipe_df.drop_duplicates(subset=DROP_DUPLICATES_BY_COLUMN, keep='first', inplace=True)
    recipe_df.reset_index(drop=True, inplace=True)
    print(recipe_df)

    # save preprocessed df
    dt_preprocess = DataPreprocessing()
    dt_preprocessed = dt_preprocess.preprocess_df(recipe_df)
    dt_preprocessed.to_csv(DATA_PARSED_CSV_PATH, sep="\t", index=False)

    test_string = "[' 22(del)5g unsalted          butter,  (delete) softened', '225g caster sugar', '4 eggs', " \
                  "'225g self,-raising flour', '1        lemon, zested', '1½ lemons, juiced', '85g caster sugar',' salt']"
    list_test_ingredients = dt_preprocess.preprocess_request(test_string)
    print(list_test_ingredients)
