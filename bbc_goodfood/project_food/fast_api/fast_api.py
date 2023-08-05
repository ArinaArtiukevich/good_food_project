from typing import List

import joblib
import pandas as pd
import uvicorn
from fastapi import FastAPI, Response, Query, status

from project_food.data_preprocessing.preprocessing import DataPreprocessing
from project_food.input_parsing.parsing import BBCRecipesParses
from project_food.recipe_model.tf_idf import TF_IDF_RecipeRecommendation
from project_food.recipe_model.word2vec import TfIdfWord2Vec, MeanWord2Vec

from project_food.constants import DATA_PATH_FULL_CSV, DATA_PATH_FULL_PICKLE, DATA_PARSED_PATH_PICKLE, DATA_PARSED_PATH_CSV, \
     DROP_DUPLICATES_BY_COLUMN, WORD2VEC_MODEL, TF_IDF_MODEL

app = FastAPI()


@app.get("/data/parse/pickle")
async def parse_recipe_pickle(path: str = DATA_PATH_FULL_PICKLE):
    parser = BBCRecipesParses()
    data = parser.parse_recipes(return_dataframe=False)
    joblib.dump(data, path)
    return Response((pd.DataFrame(data)).to_json(orient="records"), media_type="application/json")


@app.get("/data/parse/csv")
async def parse_recipe_csv(path: str = DATA_PATH_FULL_CSV):
    parser = BBCRecipesParses()
    data = parser.parse_recipes(return_dataframe=True)
    df = pd.DataFrame(data)
    df.to_csv(
        path,
        sep="\t", index=False)
    return Response(df.to_json(orient="records"), media_type="application/json")


@app.get("/data/preprocess/pickle")
async def parse_recipe_pickle(load_path: str = DATA_PATH_FULL_PICKLE, save_path: str = DATA_PARSED_PATH_PICKLE):
    recipes_list = joblib.load(load_path)
    dt_preprocess = DataPreprocessing()
    unique_recipes_list = list(set(recipes_list))
    print(unique_recipes_list)
    preprocessed_list = dt_preprocess.preprocess_list(unique_recipes_list)
    joblib.dump(preprocessed_list, save_path)

    return Response((pd.DataFrame(preprocessed_list)).to_json(orient="records"), media_type="application/json")


@app.get("/data/preprocess/csv")
async def parse_recipe_csv(load_path: str = DATA_PATH_FULL_CSV, save_path: str = DATA_PARSED_PATH_CSV):
    recipe_df = pd.read_csv(load_path, sep='\t')
    recipe_df.drop_duplicates(subset=DROP_DUPLICATES_BY_COLUMN, keep='first', inplace=True)
    recipe_df.reset_index(drop=True, inplace=True)
    dt_preprocess = DataPreprocessing()
    df_preprocessed = dt_preprocess.preprocess_df(recipe_df)
    df_preprocessed.to_csv(save_path, sep="\t", index=False)
    return Response(df_preprocessed.to_json(orient="records"), media_type="application/json")


@app.get("/recipe/tf_idf")
async def get_recipe_tf_idf(save_path: str = TF_IDF_MODEL, user_input: List[str] | None = Query()):
    model = TF_IDF_RecipeRecommendation.from_pickle(path=save_path)
    response = model.get_recommendations(str(user_input))
    return Response(response.to_json(), media_type="application/json")


@app.get("/recipe/train/tf_idf")
async def train_recipe_tf_idf(data_path: str = DATA_PARSED_PATH_CSV, save_path: str = TF_IDF_MODEL):
    model = TF_IDF_RecipeRecommendation.create_instance(from_csv=True, path=data_path).prepare_model()
    model.to_pickle(path=save_path)
    return status.HTTP_201_CREATED


@app.get("/recipe/w2v_mean")
async def get_recipe_w2v_mean(path: str = WORD2VEC_MODEL, user_input: List[str] | None = Query()):
    model = MeanWord2Vec.from_pickle(path=path)
    response = model.get_recommendations(str(user_input))
    return Response(response.to_json(), media_type="application/json")


@app.get("/recipe/train/w2v_mean")
async def train_recipe_w2v_mean(data_path: str = DATA_PARSED_PATH_CSV, save_path: str = WORD2VEC_MODEL):
    model = MeanWord2Vec.create_instance(path=data_path).train_model()
    model.to_pickle(path=save_path)
    return status.HTTP_201_CREATED


@app.get("/recipe/w2v_tf_idf")
async def get_recipe_w2v_tf_idf(path: str = WORD2VEC_MODEL, user_input: List[str] | None = Query()):
    model = TfIdfWord2Vec.from_pickle(path=path)
    response = model.get_recommendations(str(user_input))
    return Response(response.to_json(), media_type="application/json")


@app.get("/recipe/train/w2v_tf_idf")
async def train_recipe_w2v_tf_idf(data_path: str = DATA_PARSED_PATH_CSV, save_path: str = WORD2VEC_MODEL):
    model = TfIdfWord2Vec.create_instance(path=data_path).train_model()
    model.to_pickle(path=save_path)
    return status.HTTP_201_CREATED


if __name__ == "__main__":
    uvicorn.run("fast_api:app", host="127.0.0.1", port=8000, log_level="info")
