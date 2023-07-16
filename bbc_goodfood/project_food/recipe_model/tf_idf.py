from collections import defaultdict

import joblib
import numpy as np
import pandas as pd
from Levenshtein import distance
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

from constants import DATA_PARSED_PATH_CSV, INGREDIENTS_PARSED_COLUMN, INGREDIENTS_COLUMN, TF_IDF_MODEL, \
    DATA_PARSED_PATH_PICKLE, LIST_PARAMS_PARSED_MODEL
from data.schema.recommendation_models import FittedTfIdfModel
from data_preprocessing.preprocessing import DataPreprocessing


class TF_IDF_RecipeRecommendation:

    def __init__(self,
                 df: pd.DataFrame,
                 column_name: str = INGREDIENTS_PARSED_COLUMN,
                 cv: CountVectorizer = CountVectorizer(ngram_range=(1, 1), analyzer='word', lowercase=True),
                 tfidf: TfidfTransformer = TfidfTransformer(),
                 tfidf_matrix: np.ndarray = None
                 ):
        self.df = df
        self.column_name = column_name
        self.cv = cv
        self.tfidf = tfidf
        self.tfidf_matrix = tfidf_matrix

    @classmethod
    def get_df_from_csv(cls, df_path: str = DATA_PARSED_PATH_CSV) -> pd.DataFrame:
        return pd.read_csv(df_path, sep='\t')

    @classmethod
    def get_df_from_pickle(cls, list_path: str = DATA_PARSED_PATH_PICKLE) -> pd.DataFrame:
        result_df = pd.DataFrame(joblib.load(list_path))
        result_df[LIST_PARAMS_PARSED_MODEL] = result_df[LIST_PARAMS_PARSED_MODEL].apply(
            lambda x: [str(sentence) for sentence in x])
        return result_df

    @classmethod
    def create_instance(cls, from_csv: bool = True, path: str = DATA_PARSED_PATH_CSV) -> "TF_IDF_RecipeRecommendation":
        return cls(df=cls.get_df_from_csv(path)) if from_csv else cls(df=cls.get_df_from_pickle(path))

    def prepare_model(self):
        self.cv.fit(self.df[self.column_name])
        cv_table = self.cv.transform(self.df[self.column_name])
        self.tfidf_matrix = self.tfidf.fit_transform(cv_table)
        return self

    def get_cv_words_similarity(self) -> dict:
        similarity_scores = defaultdict(dict)
        for i in range(len(self.cv.get_feature_names_out())):
            similarity_scores[self.cv.get_feature_names_out()[i]] = {}
            for j in range(i + 1, len(self.cv.get_feature_names_out())):
                d = distance(self.cv.get_feature_names_out()[i], self.cv.get_feature_names_out()[j])
                similarity_scores[self.cv.get_feature_names_out()[i]][self.cv.get_feature_names_out()[j]] = d
                similarity_scores[self.cv.get_feature_names_out()[j]][self.cv.get_feature_names_out()[i]] = d

        return similarity_scores

    def get_recommendations(self, user_input: str):
        preprocessed_input = pd.Series([(DataPreprocessing().preprocess_request(user_input))]).astype(str)
        input_cv = self.cv.transform(preprocessed_input)
        input_tfidf = self.tfidf.transform(input_cv)
        # todo
        # dense_input = input_tfidf.todense()
        # dense_model = self.tfidf_ingredients.todense()

        return pd.Series(
            np.array(list((map(lambda x: cosine_similarity(input_tfidf, x), self.tfidf_matrix)))).ravel(),
            index=self.df[INGREDIENTS_COLUMN]).sort_values(ascending=False).head(5)

    def to_pickle(self, path: str = TF_IDF_MODEL):
        items = FittedTfIdfModel(
            df=self.df,
            cv=self.cv,
            tfidf=self.tfidf,
            tfidf_matrix=self.tfidf_matrix
        )
        joblib.dump(items, path)

    @classmethod
    def from_pickle(cls, path: str = TF_IDF_MODEL) -> "TF_IDF_RecipeRecommendation":
        tf_idf_model = joblib.load(path)
        return cls(tf_idf_model.df, tf_idf_model.cv, tf_idf_model.tfidf,
                   tf_idf_model.tfidf_matrix)


if __name__ == "__main__":
    tf_idf = TF_IDF_RecipeRecommendation.create_instance(from_csv=True, path=DATA_PARSED_PATH_CSV).prepare_model()
    # tf_idf = TF_IDF_RecipeRecommendation.create_instance(from_csv=False, path=DATA_PARSED_PATH_PICKLE).prepare_model()
    rec = tf_idf.get_recommendations("['cinnamon', 'sugar', 'apple', 'flour', 'butter']")
    print(rec)

    # todo del
    # pth = "/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/csv_dataframe/data_goodfood_bbc_delete.csv"
    # df = pd.read_csv(DATA_PARSED_PATH_CSV, sep='\t')
    # df['ingredients_parsed'] = df['ingredients_parsed'].apply(eval)
    # df['ingredients'] = df['ingredients'].apply(eval)
    #
    # mlb = MultiLabelBinarizer().fit(df['ingredients_parsed'])
    # print(mlb.classes_.shape)
    #
    # print(pd.DataFrame(mlb.transform(df['ingredients_parsed']), index=df.index, columns=mlb.classes_))
    # sparse_mtr = pd.DataFrame(mlb.transform(df['ingredients_parsed']), index=df.index, columns=mlb.classes_)
    #
    # sparse_mtr.to_csv(pth, sep="\t", index=False)
    #
    # print(sparse_mtr.sum().sort_values(ascending=False).head(50))
    # # sparse_mtr.sum().sort_values(ascending=False).plot(kind="bar", figsize=(10, 5))
