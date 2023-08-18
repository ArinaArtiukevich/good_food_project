DATA_PATH_SHORT_CSV = r'/app/data/csv_dataframe/data_goodfood_bbc_short.csv'
DATA_PATH_FULL_CSV = r'/app/data/csv_dataframe/data_goodfood_bbc_full.csv'
DATA_PARSED_PATH_CSV = '/app/data/csv_dataframe/data_goodfood_bbc_parsed.csv'

DATA_PATH_SHORT_PICKLE = r'/app/data/structured_data/data_goodfood_bbc_short.pickle'
DATA_PATH_FULL_PICKLE = r'/app/data/structured_data/data_goodfood_bbc_full.pickle'
DATA_PARSED_PATH_PICKLE = r'/app/data/structured_data/data_goodfood_bbc_parsed.pickle'

TF_IDF_MODEL = r'/app/data/tf_idf/tf_idf_model.pickle'
CV_MODEL = r'/app/data/tf_idf/cv_model.pickle'
WORD2VEC_MODEL_MEAN = '/app/data/word2vec/word2vec_mean.pickle'
WORD2VEC_MODEL_TF_IDF = '/app/data/word2vec/word2vec_tf_idf.pickle'

DOC2VEC_MODEL = '/app/data/doc2vec/doc2vec.pickle'

MOBILENET_V5_MODEL = '/app/data/photo2ingredients/trained_model/photo2ingredients.h5'
SLIDED_IMAGES_PATH = '/app/data/photo2ingredients/images'

SLIDED_IMAGES_FOLDER = '/slided_images/'
# TABLE_CLASS = 'table'
# TABLE_INDEX = 49
IMG_SIZE = 224
# AVAILABLE_INGREDIENT_NAMES = [
#                                  'apple', 'asparagus', 'aubergine', 'avocado', 'banana', 'beans', 'beetroot',
#                                  'cabbage', 'carrots', 'cauliflower', 'corn', 'cucumber', 'garlic', 'ginger',
#                                  'grapes', 'jalepeno', 'juice', 'kiwi', 'leek', 'lemon', 'lettuce', 'lime',
#                                  'mango', 'melon', 'milk', 'mushroom', 'nectarine', 'oat-milk', 'oatghurt',
#                                  'onion', 'orange', 'papaya', 'passion-fruit', 'peach', 'pear', 'peas',
#                                  'pepper', 'pineapple', 'plum', 'pomegranate', 'potato', 'raddish',
#                                  'red-grapefruit', 'satsumas', 'sour-cream', 'sour-milk', 'soy-milk', 'soyghurt',
#                                  'spinach', 'table', 'tomato', 'turnip', 'watermelon', 'yoghurt', 'zucchini'
#                              ]


AVAILABLE_INGREDIENT_NAMES = [
                                'apple', 'banana', 'beetroot', 'bell pepper', 'cabbage',
                                'capsicum', 'carrot', 'cauliflower', 'chilli pepper',
                                'corn', 'cucumber', 'eggplant', 'garlic', 'ginger',
                                'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce',
                                'mango', 'onion', 'orange', 'paprika', 'pear',
                                'peas', 'pineapple', 'pomegranate', 'potato',
                                'raddish', 'soy beans', 'spinach', 'sweetcorn',
                                'sweetpotato', 'tomato', 'turnip', 'watermelon'
                            ]

INGREDIENTS_COLUMN = "ingredients"
TYPES_COLUMN = "types"
NAME_COLUMN = "name"
INGREDIENTS_PARSED_COLUMN = "ingredients_parsed"

DATAFRAME_INIT_COLUMNS = ['cuisine', 'types', 'name', 'ingredients', 'difficulty', "health_banners", 'instructions',
                          'link']
DROP_DUPLICATES_BY_COLUMN = INGREDIENTS_COLUMN
LIST_PARAMS_PARSED_MODEL = ['cuisine', 'types', 'health_banners', 'ingredients_parsed', 'instructions', 'link']

# BOT
DEFAULT_RECOMMENDATION_OPTION = "default"
TF_IDF_RECOMMENDATION_OPTION = "tf_idf"
W2V_MEAN_RECOMMENDATION_OPTION = "w2v_mean"
W2V_TF_IDF_RECOMMENDATION_OPTION = "w2v_tf_idf"

# todo del secure data
# BOT_TOKEN = '6421904425:AAH22gBs6bGYVZ2XekeO5yqmReXkJMyS3n0'
# BOT_USERNAME = '@recipe_recommender_bot'
# FAST_API_URL = f'http://localhost:8000'
