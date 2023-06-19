import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer

from constants import DATA_PARSED_CSV_PATH, TF_IDF_RECIPE_RECOMMENDATION_MODEL, TF_IDF_INGREDIENT_RECIPE_RECOMMENDATION, \
    CV_MODEL
from preprocessing.preprocessing import DataPreprocessing


class TF_IDF_RecipeRecommendation:

    def __init__(self, df_path: str = DATA_PARSED_CSV_PATH,
                 cv: CountVectorizer = CountVectorizer(ngram_range=(1, 1), lowercase=True),
                 tfidf: TfidfTransformer = TfidfTransformer()):
        self.df_path = df_path
        self.df = pd.read_csv(df_path, sep='\t')
        self.cv = cv
        self.tfidf = tfidf

    def prepare_model(self):
        self.cv.fit(self.df["ingredients_parsed"])
        cv_table = self.cv.transform(self.df["ingredients_parsed"])
        joblib.dump(self.cv, CV_MODEL)

        # self.tfidf.fit(cv_table)
        tfidf_ingredients = self.tfidf.fit_transform(cv_table)
        joblib.dump(self.tfidf, TF_IDF_RECIPE_RECOMMENDATION_MODEL)
        joblib.dump(tfidf_ingredients, TF_IDF_INGREDIENT_RECIPE_RECOMMENDATION)

        # todo
        # pd.DataFrame.sparse.from_spmatrix(tfidf_ingredients, index=df["ingredients_parsed"],
        #                                   columns=cv.get_feature_names_out())
        # tfidf = TfidfVectorizer()
        # tfidf.fit(df['ingredients_parsed'])
        # tfid_model = tfidf.transform(df['ingredients_parsed'])
        return self


class CosineRecommendationModel:
    # todo TRAIN TEST
    def __init__(self, original_data: pd.DataFrame, tf_idf_model_path: str = TF_IDF_RECIPE_RECOMMENDATION_MODEL,
                 tf_idf_ingredients_path: str = TF_IDF_INGREDIENT_RECIPE_RECOMMENDATION,
                 cv_path: str = CV_MODEL):
        self.df = original_data
        self.tf_idf_path = tf_idf_model_path
        self.tf_idf_ingredients_path = tf_idf_ingredients_path
        self.cv_path = cv_path
        self.tfidf = joblib.load(self.tf_idf_path)
        self.tfidf_ingredients = joblib.load(self.tf_idf_ingredients_path)
        self.cv = joblib.load(self.cv_path)

    def get_recommendations(self, user_input: str):
        preprocessed_input = pd.Series([(DataPreprocessing().preprocess_request(user_input))]).astype(str)
        print(preprocessed_input)
        input_cv = self.cv.transform(preprocessed_input)
        input_tfidf = self.tfidf.transform(input_cv)
        # todo
        # dense_input = input_tfidf.todense()
        # dense_model = self.tfidf_ingredients.todense()

        return pd.Series(
            np.array(list((map(lambda x: cosine_similarity(input_tfidf, x), self.tfidf_ingredients)))).ravel(),
            index=self.df["ingredients"]).sort_values(ascending=False).head(5)


if __name__ == "__main__":
    tf_idf = TF_IDF_RecipeRecommendation().prepare_model()
    cr = CosineRecommendationModel(tf_idf.df)
    rec = cr.get_recommendations("['cinnamon', 'vinegar']")
    print(rec)