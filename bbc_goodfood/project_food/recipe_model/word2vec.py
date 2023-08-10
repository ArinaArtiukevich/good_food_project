import ast
from collections import defaultdict

import joblib
import numpy as np
import pandas as pd
from typing import List, Dict
from gensim.models.word2vec import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys

sys.path.append("..")
from configs.constants import DATA_PARSED_PATH_CSV, INGREDIENTS_COLUMN, WORD2VEC_MODEL_MEAN, WORD2VEC_MODEL_TF_IDF, \
    INGREDIENTS_PARSED_COLUMN, NAME_COLUMN
from data.schema.recommendation_models import NamedWord2Vec
from data_preprocessing.preprocessing import DataPreprocessing
from recipe_model.basic_model import BasicModel


class CustomWord2Vec(BasicModel):
    def __init__(self, df: pd.DataFrame, w2v_model: Word2Vec = None, val: List = None):
        self.df = df
        self.w2v_model = w2v_model
        self.val = val

    def get_and_sort_corpus(self, data):
        corpus_sorted = []
        for doc in data:
            doc.sort()
            sorted_sentences = [' '.join(sorted(sentence.split())) for sentence in doc]
            corpus_sorted.append(sorted_sentences)
        return corpus_sorted

    def train_model(self):
        self.val = [[word for sentence in ast.literal_eval(ingredients) for word in sentence.split()] for ingredients in
                    self.df[INGREDIENTS_PARSED_COLUMN].values]
        self.val = self.get_and_sort_corpus(self.val)
        self.w2v_model = Word2Vec(
            sg=0, workers=1, window=2, min_count=2
        )
        self.w2v_model.build_vocab(self.val)
        self.w2v_model.train(self.val, total_examples=self.w2v_model.corpus_count, epochs=30)

        return self

    def fit(self):
        ...

    def transform(self, val: List):
        ...

    def get_recommendations(self, user_input: str) -> pd.Series:
        ...

    def to_pickle(self, path: WORD2VEC_MODEL_MEAN):
        items = NamedWord2Vec(
            df=self.df,
            w2v_model=self.w2v_model,
            val=self.val
        )
        joblib.dump(items, path)

    @classmethod
    def from_pickle(cls, path: WORD2VEC_MODEL_MEAN) -> "CustomWord2Vec":
        w2v_model = joblib.load(path)
        return cls(w2v_model.df, w2v_model.w2v_model, w2v_model.val)


class MeanWord2Vec(CustomWord2Vec):
    def __init__(self, df: pd.DataFrame, w2v_model: Word2Vec = None, val: List = None):
        super().__init__(df, w2v_model, val)

    @classmethod
    def create_instance(cls, from_csv: bool = True, path: str = DATA_PARSED_PATH_CSV) -> "MeanWord2Vec":
        return cls(df=cls.get_df_from_csv(path)) if from_csv else cls(df=cls.get_df_from_pickle(path))

    def fit(self):
        return self

    def transform(self, val: List):
        return np.vstack([self.doc_average(doc) for doc in val])

    def doc_average(self, doc: List):
        mean = []
        for word in doc:
            if word in self.w2v_model.wv.index_to_key:
                mean.append(self.w2v_model.wv.get_vector(word))
        if not mean:
            return np.zeros(self.w2v_model.wv.vector_size)
        else:
            mean = np.array(mean).mean(axis=0)
            return mean

    def get_recommendations(self, user_input: str) -> pd.Series:
        preprocessed_input = self.get_and_sort_corpus([DataPreprocessing().preprocess_request(user_input)])
        transformed_input = self.transform(preprocessed_input)
        doc_model = self.fit().transform(self.val)
        doc_model = [doc.reshape(1, -1) for doc in doc_model]
        cos_sim = map(lambda x: cosine_similarity(transformed_input, x)[0][0], doc_model)
        scores = list(cos_sim)

        return pd.Series(
            np.array(list((map(lambda x: cosine_similarity(transformed_input, x), doc_model)))).ravel(),
            index=[self.df[NAME_COLUMN], self.df[INGREDIENTS_COLUMN]]).sort_values(ascending=False).head(5)


class TfIdfWord2Vec(CustomWord2Vec):
    def __init__(self, df: pd.DataFrame, w2v_model: Word2Vec = None, val: List = None, word_idf_weight: Dict = None):
        super().__init__(df, w2v_model, val)
        self.word_idf_weight = word_idf_weight

    @classmethod
    def create_instance(cls, from_csv: bool = True, path: str = DATA_PARSED_PATH_CSV) -> "TfIdfWord2Vec":
        return cls(df=cls.get_df_from_csv(path)) if from_csv else cls(df=cls.get_df_from_pickle(path))

    def train_model(self):
        self.val = [[word for sentence in ast.literal_eval(ingredients) for word in sentence.split()] for ingredients in
                    self.df[INGREDIENTS_PARSED_COLUMN].values]
        # self.val = [ast.literal_eval(ingredients) for ingredients in self.df[INGREDIENTS_PARSED_COLUMN].values]
        # todo same with input
        # can be with or without
        self.val = self.get_and_sort_corpus(self.val)
        self.w2v_model = Word2Vec(
            sg=0, workers=1, window=2, min_count=2
        )
        self.w2v_model.build_vocab(self.val)
        self.w2v_model.train(self.val, total_examples=self.w2v_model.corpus_count, epochs=30)

        return self

    def fit(self):
        text_recipies = []
        for recipe in self.val:
            text_recipies.append(" ".join(recipe))

        tfidf = TfidfVectorizer()
        tfidf.fit(text_recipies)
        max_idf = max(tfidf.idf_)
        self.word_idf_weight = defaultdict(
            lambda: max_idf,
            [(word, tfidf.idf_[i]) for word, i in tfidf.vocabulary_.items()],
        )
        return self

    def transform(self, vals: List):
        return np.vstack([self.word_average(val) for val in vals])

    def word_average(self, sent):
        mean = []
        for word in sent:
            if word in self.w2v_model.wv.index_to_key:
                mean.append(
                    self.w2v_model.wv.get_vector(word) * self.word_idf_weight[word]
                )

        if not mean:
            return np.zeros(self.w2v_model.wv.vector_size)
        else:
            mean = np.array(mean).mean(axis=0)
            return mean

    def get_recommendations(self, user_input: str) -> pd.Series:
        doc_model = self.fit().transform(self.val)
        doc_model = [doc.reshape(1, -1) for doc in doc_model]

        preprocessed_input = self.get_and_sort_corpus([DataPreprocessing().preprocess_request(user_input)])
        transformed_input = self.transform(preprocessed_input)

        cos_sim = map(lambda x: cosine_similarity(transformed_input, x)[0][0], doc_model)
        scores = list(cos_sim)

        return pd.Series(
            np.array(list((map(lambda x: cosine_similarity(transformed_input, x), doc_model)))).ravel(),
            index=[self.df[NAME_COLUMN], self.df[INGREDIENTS_COLUMN]]).sort_values(ascending=False).head(5)


if __name__ == "__main__":
    # model = MeanWord2Vec.create_instance().train_model()
    #
    # # print(model.w2v_model)
    # # words = list(model.w2v_model.wv.index_to_key)
    # # words.sort()
    # # print(words)
    # # print(model.w2v_model.wv['chicken stock'])
    # # print(model.w2v_model.wv.most_similar(u'cinnamon'))
    # # print(model.w2v_model.wv.similarity('coconut yogurt', 'yogurt'))
    #
    # user_inp = "['cinnamon', 'sugar', 'apple', 'flour', 'butter']"
    # rec = model.get_recommendations(user_inp)
    # print(rec)

    tfidf_word_to_vec = TfIdfWord2Vec.create_instance().train_model()
    user_inp = "['cinnamon', 'sugar', 'apple', 'flour', 'butter']"
    rec = tfidf_word_to_vec.get_recommendations(user_inp)
    print(rec)

    tfidf_word_to_vec.to_pickle()
    tfidf_word_to_vec.from_pickle()
