import sys
from io import BytesIO
from typing import List

import joblib
import pandas as pd
import uvicorn
from PIL import Image

sys.path.append("..")
from fastapi import FastAPI, Response, Query, status, UploadFile, File
from data_preprocessing.preprocessing import DataPreprocessing
from input_parsing.parsing import BBCRecipesParses
from recipe_model.tf_idf import TF_IDF_RecipeRecommendation
from recipe_model.word2vec import TfIdfWord2Vec, MeanWord2Vec
from recipe_model.doc2vec import CustomDoc2Vec
from recipe_model.photo2ingredients import Photo2Ingredients, Photo2MultipleIngredients
from configs.constants import DATA_PATH_FULL_CSV, DATA_PATH_FULL_PICKLE, DATA_PARSED_PATH_PICKLE, DATA_PARSED_PATH_CSV, \
    DROP_DUPLICATES_BY_COLUMN, WORD2VEC_MODEL_MEAN, WORD2VEC_MODEL_TF_IDF, TF_IDF_MODEL, DOC2VEC_MODEL

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
async def get_recipe_w2v_mean(path: str = WORD2VEC_MODEL_MEAN, user_input: List[str] | None = Query()):
    model = MeanWord2Vec.from_pickle(path=path)
    response = model.get_recommendations(str(user_input))
    return Response(response.to_json(), media_type="application/json")


@app.get("/recipe/train/w2v_mean")
async def train_recipe_w2v_mean(data_path: str = DATA_PARSED_PATH_CSV, save_path: str = WORD2VEC_MODEL_MEAN):
    model = MeanWord2Vec.create_instance(path=data_path).train_model()
    model.to_pickle(path=save_path)
    return status.HTTP_201_CREATED


@app.get("/recipe/w2v_tf_idf")
async def get_recipe_w2v_tf_idf(path: str = WORD2VEC_MODEL_TF_IDF, user_input: List[str] | None = Query()):
    model = TfIdfWord2Vec.from_pickle(path=path)
    response = model.get_recommendations(str(user_input))
    return Response(response.to_json(), media_type="application/json")


@app.get("/recipe/train/w2v_tf_idf")
async def train_recipe_w2v_tf_idf(data_path: str = DATA_PARSED_PATH_CSV, save_path: str = WORD2VEC_MODEL_TF_IDF):
    model = TfIdfWord2Vec.create_instance(path=data_path).train_model()
    model.to_pickle(path=save_path)
    return status.HTTP_201_CREATED


@app.post("/photo2ingredients")
async def get_ingredient_from_photo(image: UploadFile = File(...)):
    image_bytes = await image.read()
    image_pil = Image.open(BytesIO(image_bytes))
    img2ingredients = Photo2Ingredients()
    return img2ingredients.predict_ingredients(image_pil)


@app.post("/photo2multiple_ingredients")
async def get_ingredients_from_photo(image: UploadFile = File(...)):
    image_bytes = await image.read()
    image_pil = Image.open(BytesIO(image_bytes))
    img2ingredients = Photo2MultipleIngredients()
    return img2ingredients.predict_ingredients(image_pil)


@app.get("/recipe/doc2vec")
async def get_recipe_d2v(path: str = DOC2VEC_MODEL, user_input: List[str] | None = Query()):
    model = CustomDoc2Vec.from_pickle(path=path)
    response = model.get_recommendations(str(user_input))
    result_dict = {}
    for idx, row in response.iterrows():
        row_values = row.values.tolist()
        result_dict[str(tuple(row_values))] = idx
    return result_dict


@app.get("/recipe/doc2vec/category")
async def get_recipe_d2v_category(category: str, path: str = DOC2VEC_MODEL, user_input: List[str] | None = Query()):
    model = CustomDoc2Vec.from_pickle(path=path)
    response = model.get_recommendations(str(user_input), category=category).head(5)
    result_dict = {}
    for idx, row in response.iterrows():
        row_values = row.values.tolist()
        result_dict[str(tuple(row_values))] = idx
    return result_dict


@app.get("/recipe/train/doc2vec")
async def train_recipe_doc2vec(data_path: str = DATA_PARSED_PATH_CSV, save_path: str = DOC2VEC_MODEL):
    model = CustomDoc2Vec.create_instance(path=data_path).train_model()
    model.to_pickle(path=save_path)
    return status.HTTP_201_CREATED


if __name__ == "__main__":
    uvicorn.run("fast_api:app", host="0.0.0.0", port=8000, log_level="info")
