from typing import NamedTuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


class FittedTfIdfModel(NamedTuple):
    df: pd.DataFrame
    cv: CountVectorizer
    tfidf: TfidfTransformer
    tfidf_matrix: np.ndarray
