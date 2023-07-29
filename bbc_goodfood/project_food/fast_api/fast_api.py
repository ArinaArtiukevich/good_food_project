from typing import List

import joblib
import pandas as pd
from fastapi import FastAPI, Response, Query

from constants import DATA_PATH_FULL_CSV, DATA_PATH_FULL_PICKLE
from input_parsing.parsing import BBCRecipesParses
from recipe_model.word2vec import TfIdfWord2Vec

app = FastAPI()
@app.get("/parse/pickle")
async def parse_recipe_pickle():
    parser = BBCRecipesParses()
    data = parser.parse_recipes(return_dataframe=False)
    joblib.dump(data, DATA_PATH_FULL_PICKLE)
    return Response((pd.DataFrame(data)).to_json(orient="records"), media_type="application/json")


@app.get("/parse/csv")
async def parse_recipe_csv():
    parser = BBCRecipesParses()
    data = parser.parse_recipes(return_dataframe=True)
    df = pd.DataFrame(data)
    df.to_csv(
        DATA_PATH_FULL_CSV,
        sep="\t", index=False)
    return Response(df.to_json(orient="records"), media_type="application/json")

# @app.get("/preprocess")
# async def preprocess_ingredients():
#


# @app.get("/recipe/tf_idf")
# async def get_recipe_tf_idf():
#     response = currency_exchange.df_prettifier(df)
#     return response.encode('utf-8')

#
# @app.get("/recipe/w2v_mean")
# async def get_recipe_w2v_mean():
#     response = currency_exchange.df_prettifier(df)
#     return response.encode('utf-8')
#
#
@app.get("/recipe/w2v_tf_idf")
async def get_recipe_w2v_tf_idf(user_input: List[str] | None = Query()):
    # todo divide training/ getting result
    tfidf_word_to_vec = TfIdfWord2Vec.create_instance().train_model()
    response = tfidf_word_to_vec.get_recommendations(str(user_input))
    return Response(response.to_json(), media_type="application/json")


