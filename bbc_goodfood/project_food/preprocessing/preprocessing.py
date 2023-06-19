import pandas as pd
import re
import nltk
# nltk.download('stopwords')
# nltk.download('omw-1.4')

from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
# todo delete SnowballStemmer - более "сильный"
from typing import List
from constants import DATA_CSV_PATH, DATA_PARSED_CSV_PATH


class DataPreprocessing:
    MEASURES = ['cup', 'tsp', 'tbsp', 'c', 'fl oz', 'pt', 'qt', 'gal', 'g', 'kg', 'mg', 'oz', 'lb', 'slice', 'piece',
                'pinch', 'dash', 'whole', 'dozen', 'count', 'pkg', 'can', 'jar', 'carton', 'stick', 'drop', 'cm', 'm',
                'ml', 'l', 'x', 'pint', 'cubes', 'cube', 'pack']
    # STOP_WORDS = ['a', 'an', 'the', 'in', 'on', 'at', 'for', 'of', 'with', 'to', 'from', 'by', 'as', 'is', 'are',
    # 'was', 'were', 'has', 'have', 'had', 'need']
    STOP_WORDS = set(nltk.corpus.stopwords.words('english') + ['new', "%"])
    PATTERN_REMOVE_DIGITS_BRACKETS = r'(\d|\½|¼)(\-?\.?)\s?|\((.*?)\)|\\u'
    PATTERN_JOIN_WORDS = r'\b(?:{})\s?\b'
    PATTERN_SPLIT_WORDS = r'\W+|\s+'

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = SnowballStemmer("english")

    def create_pattern(self, join_pattern: str, words: List[str]) -> str:
        return join_pattern.format('|'.join(words))

    # TODO join prettify_string_ingredients and prettify_df_ingredients ???
    def prettify_string_ingredients(self, input_string: str) -> List:
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
        return eval(modified_string)

    def prettify_df_ingredients(self, df_recipes: pd.DataFrame) -> pd.DataFrame:
        df = df_recipes.copy()
        # df["ingredients"] - str

        # lower case
        df["ingredients"] = df["ingredients"].str.lower()

        # remove numbers + "("..")" + u2028
        df["ingredients"] = df["ingredients"].str.replace(self.PATTERN_REMOVE_DIGITS_BRACKETS, "", regex=True)

        # measures
        pattern = self.create_pattern(self.PATTERN_JOIN_WORDS, self.MEASURES)
        df["ingredients"] = df["ingredients"].str.replace(pattern, "", regex=True)

        # stop_words
        pattern = self.create_pattern(self.PATTERN_JOIN_WORDS, list(self.STOP_WORDS))
        df["ingredients"] = df["ingredients"].str.replace(pattern, "", regex=True)

        # create list from string
        df['ingredients'] = df['ingredients'].apply(eval).tolist()

        return df

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
        prettified_df = self.prettify_df_ingredients(df)
        result_df['ingredients_parsed'] = prettified_df['ingredients'].apply(lambda x: self.preprocess_list_ingredients(x))
        result_df.to_csv(DATA_PARSED_CSV_PATH, sep="\t", index=False)
        return result_df


if __name__ == "__main__":
    df = pd.read_csv(DATA_CSV_PATH, sep='\t')
    recipe_df = df.copy()
    print(recipe_df.shape)
    recipe_df.sort_values("name", inplace=True)
    recipe_df.drop_duplicates(subset="name", keep=False, inplace=True)
    recipe_df.reset_index(drop=True, inplace=True)
    print(recipe_df)

    dt_preprocess = DataPreprocessing()
    print(dt_preprocess.preprocess_df(recipe_df))

    test_string = "['22(del)5g unsalted butter,  (delete) softened', '225g caster sugar', '4 eggs', " \
                  "'225g self-raising flour', '1 lemon, zested', '1½ lemons, juiced', '85g caster sugar']"
    list_test_ingredients = dt_preprocess.preprocess_request(test_string)
    print(list_test_ingredients)
