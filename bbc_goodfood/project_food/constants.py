DATA_PATH_SHORT_CSV = r'/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/csv_dataframe/data_goodfood_bbc_short.csv'
DATA_PATH_FULL_CSV = r'/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/csv_dataframe/data_goodfood_bbc_full.csv'
DATA_PARSED_PATH_CSV = r'/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/csv_dataframe/data_goodfood_bbc_parsed.csv'

DATA_PATH_SHORT_PICKLE = r'/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/structured_data/data_goodfood_bbc_short.pickle'
DATA_PATH_FULL_PICKLE = r'/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/structured_data/data_goodfood_bbc_full.pickle'
DATA_PARSED_PATH_PICKLE = r'/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/structured_data/data_goodfood_bbc_parsed.pickle'

TF_IDF_MODEL = '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/tf_idf/tf_idf_model.pickle'
CV_MODEL = r'/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/tf_idf/cv_model.pickle'
WORD2VEC_MODEL = '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/word2vec/word2vec.pickle'

INGREDIENTS_COLUMN = "ingredients"
INGREDIENTS_PARSED_COLUMN = "ingredients_parsed"
DATAFRAME_INIT_COLUMNS = ['cuisine', 'types', 'name', 'ingredients', 'difficulty', "health_banners"]
DROP_DUPLICATES_BY_COLUMN = INGREDIENTS_COLUMN
LIST_PARAMS_PARSED_MODEL = ['cuisine', 'types', 'health_banners', 'ingredients_parsed']

# BOT
TELEGRAM_INPUT = "Hello! Please, tell me what ingredients you have, so that I can recommend dishes.\n "\
                 "Enter command /cancel to stop the conversation.\n\n"
TELEGRAM_USER_EXAMPLE_SWEET = "cinnamon, sugar, apple"
TELEGRAM_USER_EXAMPLE_VEGETABLE = "pepper, oil, cucumber"
DEFAULT_RECOMMENDATION_OPTION = "default"
TF_IDF_RECOMMENDATION_OPTION = "tf_idf"
W2V_MEAN_RECOMMENDATION_OPTION = "w2v_mean"
W2V_TF_IDF_RECOMMENDATION_OPTION = "w2v_tf_idf"


# todo del secure data
# BOT_TOKEN = '6421904425:AAH22gBs6bGYVZ2XekeO5yqmReXkJMyS3n0'
# BOT_USERNAME = '@recipe_recommender_bot'
# FAST_API_URL = f'http://localhost:8000'

