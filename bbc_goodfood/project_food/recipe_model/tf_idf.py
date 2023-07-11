import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from constants import DATA_PARSED_PATH_CSV, INGREDIENTS_PARSED_COLUMN, INGREDIENTS_COLUMN, TF_IDF_MODEL
from data.schema.recommendation_models import FittedTfIdfModel
from data_preprocessing.preprocessing import DataPreprocessing

class TF_IDF_RecipeRecommendation:

    def __init__(self,
                 df: pd.DataFrame,
                 column_name: str = INGREDIENTS_PARSED_COLUMN,
                 cv: CountVectorizer = CountVectorizer(ngram_range=(1, 1), lowercase=True),
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
    def create_instance(cls, df_path: str = DATA_PARSED_PATH_CSV) -> "TF_IDF_RecipeRecommendation":
        return cls(df=cls.get_df_from_csv(df_path))

    def prepare_model(self):
        self.cv.fit(self.df[self.column_name])
        cv_table = self.cv.transform(self.df[self.column_name])
        self.tfidf_matrix = self.tfidf.fit_transform(cv_table)
        return self

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
        return cls(tf_idf_model.df, tf_idf_model.cv, tf_idf_model.tf_idf,
                   tf_idf_model.tfidf_matrix)


if __name__ == "__main__":
    tf_idf = TF_IDF_RecipeRecommendation.create_instance(df_path=DATA_PARSED_PATH_CSV).prepare_model()
    rec = tf_idf.get_recommendations("['cinnamon', 'sugar', 'apple', 'flour']")
    print(rec)
