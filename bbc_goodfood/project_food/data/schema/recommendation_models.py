from typing import NamedTuple, Dict, List

import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


class FittedTfIdfModel(NamedTuple):
    df: pd.DataFrame
    cv: CountVectorizer
    tfidf: TfidfTransformer
    tfidf_matrix: np.ndarray


class NamedWord2Vec(NamedTuple):
    df: pd.DataFrame
    w2v_model: Word2Vec
    val: List

