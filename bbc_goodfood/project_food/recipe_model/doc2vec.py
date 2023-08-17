import joblib
import ast
import pandas as pd

from gensim.models.doc2vec import Doc2Vec, TaggedDocument

import sys

from pandas import DataFrame

sys.path.append("..")
from configs.constants import INGREDIENTS_PARSED_COLUMN, DOC2VEC_MODEL, DATA_PARSED_PATH_CSV, INGREDIENTS_COLUMN, \
    NAME_COLUMN, TYPES_COLUMN
from recipe_model.basic_model import BasicModel
from data_preprocessing.preprocessing import DataPreprocessing
from data.schema.recommendation_models import NamedDoc2Vec


class CustomDoc2Vec(BasicModel):
    def __init__(self, df: pd.DataFrame, d2v_model: Doc2Vec = None):
        self.df = df
        self.d2v_model = d2v_model

    def train_model(self):
        ingredients_data = self.df[INGREDIENTS_PARSED_COLUMN].tolist()
        tagged_data = [
            TaggedDocument(
                words=[
                    word
                    for ingredient in ast.literal_eval(ingredients)
                    for word in ingredient.split()
                ],
                tags=[str(index)]
            )
            for index, ingredients in enumerate(ingredients_data)
        ]
        self.d2v_model = Doc2Vec(vector_size=100, window=5, min_count=1, dm=1)
        self.d2v_model.build_vocab(tagged_data)
        self.d2v_model.train(tagged_data, total_examples=self.d2v_model.corpus_count, epochs=20)
        return self

    def get_recommendations(self, user_input: str, category: str = None) -> DataFrame:
        user_input_list = DataPreprocessing().preprocess_request(user_input)
        embeddings = self.d2v_model.infer_vector(user_input_list)
        if category is None:
            best_recipes = self.d2v_model.dv.most_similar([embeddings], topn=5)
            ids = [row_id[0] for row_id in best_recipes]
            selected_rows = self.df.iloc[ids]
        else:
            print("2")
            best_recipes = self.d2v_model.dv.most_similar([embeddings], topn=200)
            doc_indices = [int(doc_idx) for doc_idx, _ in best_recipes]
            new_df = self.df.loc[doc_indices].copy()
            new_df[TYPES_COLUMN] = new_df[TYPES_COLUMN].apply(
                lambda lst_str: ast.literal_eval(lst_str) if isinstance(lst_str, str) else lst_str)
            boolean_series = new_df[TYPES_COLUMN].apply(lambda lst: category in lst if isinstance(lst, list) else False)
            selected_rows = new_df[boolean_series]
        print(selected_rows)
        selected_columns = [NAME_COLUMN, INGREDIENTS_COLUMN]
        selected_list = [selected_rows[column] for column in selected_columns]
        return pd.concat(selected_list, axis=1)

    def to_pickle(self, path: DOC2VEC_MODEL):
        items = NamedDoc2Vec(
            df=self.df,
            d2v_model=self.d2v_model,
        )
        joblib.dump(items, path)

    @classmethod
    def from_pickle(cls, path: DOC2VEC_MODEL) -> "CustomDoc2Vec":
        d2v_model = joblib.load(path)
        return cls(d2v_model.df, d2v_model.d2v_model)

    @classmethod
    def create_instance(cls, from_csv: bool = True, path: str = DATA_PARSED_PATH_CSV) -> "CustomDoc2Vec":
        return cls(df=cls.get_df_from_csv(path)) if from_csv else cls(df=cls.get_df_from_pickle(path))


if __name__ == "__main__":
    model = CustomDoc2Vec.create_instance().train_model()
    user_inp = "['cinnamon', 'sugar', 'apple', 'flour', 'butter']"
    # rec = model.get_recommendations(user_inp)
    # print(rec)

    model.to_pickle(DOC2VEC_MODEL)
    model = CustomDoc2Vec.from_pickle(DOC2VEC_MODEL)
    rec = model.get_recommendations(user_inp)
    print(rec)
