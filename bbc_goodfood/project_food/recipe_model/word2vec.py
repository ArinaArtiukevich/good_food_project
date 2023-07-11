import ast

import joblib
import pandas as pd
from gensim.models.word2vec import Word2Vec

from constants import DATA_PARSED_CSV_PATH_CSV, WORD2VEC_MODEL


class CustomWord2Vec:
    def __init__(self, df_path: str = DATA_PARSED_CSV_PATH_CSV):
        self.df_path = df_path
        self.df = pd.read_csv(df_path, sep='\t')
        self.set_model()
        self.w2v_model: Word2Vec

    def set_model(self):
        # val = [[word for sentence in ast.literal_eval(ingredients) for word in sentence.split()] for ingredients in self.df["ingredients_parsed"].values]
        val = [ast.literal_eval(ingredients) for ingredients in self.df["ingredients_parsed"].values]

        print(val)
        self.w2v_model = Word2Vec(
            val, sg=0, workers=2, window=2, min_count=3, sample=6e-5, alpha=0.03,
                     min_alpha=0.0007
        )
        self.w2v_model.train(val, total_examples=self.w2v_model.corpus_count, epochs=30, report_delay=1)

        joblib.dump(self.w2v_model, WORD2VEC_MODEL)
        self.w2v_model.save("ingredients_parsed_model")

        print(self.w2v_model.wv['egg'])
        print(self.w2v_model.wv.most_similar('egg'))
        print(self.w2v_model.wv.index_to_key)


if __name__ == "__main__":
    CustomWord2Vec()

