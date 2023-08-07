import json
import os
import sys
import uvicorn
import requests

from fastapi import FastAPI, Query, Response
from typing import List

from project_food.constants import TF_IDF_MODEL, TF_IDF_RECOMMENDATION_OPTION, DATA_PARSED_PATH_CSV, WORD2VEC_MODEL, \
    W2V_MEAN_RECOMMENDATION_OPTION, W2V_TF_IDF_RECOMMENDATION_OPTION

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import configs.dev as dev

app = FastAPI()


@app.get("/parse")
async def parse_data() -> List:
    request = dev.FAST_API_RECOMMENDER_URL + '/data/parse/csv'
    response = requests.get(request)
    return json.loads(response.text)


@app.get("/preprocess")
async def preprocess_data() -> List:
    request = dev.FAST_API_RECOMMENDER_URL + '/data/preprocess/csv'
    response = requests.get(request)
    return json.loads(response.text)


@app.get("/tf_idf")
async def get_recipe_tf_idf(save_path: str = TF_IDF_MODEL, user_input: List[str] | None = Query()):
    params = {
        'save_path': save_path,
        'user_input': user_input
    }
    request = dev.FAST_API_RECOMMENDER_URL + '/recipe/' + TF_IDF_RECOMMENDATION_OPTION
    response = requests.get(request, params)
    return response.text


@app.get("/train/tf_idf")
async def train_recipe_tf_idf(data_path: str = DATA_PARSED_PATH_CSV, save_path: str = TF_IDF_MODEL):
    params = {
        'data_path': data_path,
        'save_path': save_path
    }
    request = dev.FAST_API_RECOMMENDER_URL + '/recipe/train/' + TF_IDF_RECOMMENDATION_OPTION
    response = requests.get(request, params)
    return response.status_code


@app.get("/w2v_mean")
async def get_recipe_w2v_mean(path: str = WORD2VEC_MODEL, user_input: List[str] | None = Query()):
    params = {
        'path': path,
        'user_input': user_input
    }
    request = dev.FAST_API_RECOMMENDER_URL + '/recipe/' + W2V_MEAN_RECOMMENDATION_OPTION
    response = requests.get(request, params)
    return response.text


@app.get("/train/w2v_mean")
async def train_recipe_w2v_mean(data_path: str = DATA_PARSED_PATH_CSV, save_path: str = WORD2VEC_MODEL):
    params = {
        'data_path': data_path,
        'save_path': save_path
    }
    request = dev.FAST_API_RECOMMENDER_URL + '/recipe/train/' + W2V_MEAN_RECOMMENDATION_OPTION
    response = requests.get(request, params)
    return response.status_code


@app.get("/w2v_tf_idf")
async def get_recipe_w2v_tf_idf(path: str = WORD2VEC_MODEL, user_input: List[str] | None = Query()):
    params = {
        'path': path,
        'user_input': user_input
    }
    request = dev.FAST_API_RECOMMENDER_URL + '/recipe/' + W2V_TF_IDF_RECOMMENDATION_OPTION
    response = requests.get(request, params)
    print(response.text)
    return response.text


@app.get("/train/w2v_tf_idf")
async def train_recipe_w2v_tf_idf(data_path: str = DATA_PARSED_PATH_CSV, save_path: str = WORD2VEC_MODEL):
    params = {
        'data_path': data_path,
        'save_path': save_path
    }
    request = dev.FAST_API_RECOMMENDER_URL + '/recipe/train/' + W2V_TF_IDF_RECOMMENDATION_OPTION
    response = requests.get(request, params)
    return response.status_code


if __name__ == "__main__":
    uvicorn.run("fast_api:app", host="127.0.0.1", port=4000, log_level="info")
