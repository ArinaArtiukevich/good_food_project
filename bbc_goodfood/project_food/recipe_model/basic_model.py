import sys

import joblib
import pandas as pd

sys.path.append("..")
from configs.constants import DATA_PARSED_PATH_CSV, DATA_PARSED_PATH_PICKLE, LIST_PARAMS_PARSED_MODEL


class BasicModel:
    @classmethod
    def get_df_from_csv(cls, df_path: str = DATA_PARSED_PATH_CSV) -> pd.DataFrame:
        return pd.read_csv(df_path, sep='\t')

    @classmethod
    def get_df_from_pickle(cls, list_path: str = DATA_PARSED_PATH_PICKLE) -> pd.DataFrame:
        result_df = pd.DataFrame(joblib.load(list_path))
        result_df[LIST_PARAMS_PARSED_MODEL] = result_df[LIST_PARAMS_PARSED_MODEL].apply(
            lambda x: [str(sentence) for sentence in x])
        return result_df
