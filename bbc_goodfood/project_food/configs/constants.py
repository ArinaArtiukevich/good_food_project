DATA_PATH_FULL_CSV = r'/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/csv_dataframe/data_goodfood_bbc_full.csv'
DATA_PARSED_PATH_CSV = '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/csv_dataframe/data_goodfood_bbc_parsed.csv'

DATA_PATH_FULL_PICKLE = r'/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/structured_data/data_goodfood_bbc_full.pickle'
DATA_PARSED_PATH_PICKLE = r'/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/structured_data/data_goodfood_bbc_parsed.pickle'

TF_IDF_MODEL = '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/tf_idf/tf_idf_model.pickle'
CV_MODEL = r'/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/tf_idf/cv_model.pickle'
WORD2VEC_MODEL_MEAN = '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/word2vec/word2vec_mean.pickle'
WORD2VEC_MODEL_TF_IDF = '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/word2vec/word2vec_tf_idf.pickle'

DOC2VEC_MODEL = '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/doc2vec/doc2vec.pickle'

MOBILENET_V5_MODEL = '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/photo2ingredients/trained_model/mobilenet_model.h5'
VGG16_MODEL = '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/photo2ingredients/trained_model/vgg_model.h5'
SLIDED_IMAGES_PATH = '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/photo2ingredients/images'
SLIDED_IMAGES_FOLDER = '/slided_images/'

IMG_SIZE = 224

AVAILABLE_INGREDIENT_NAMES = [
    'apple', 'banana', 'beans_soy', 'beetroot', 'cabbage', 'carrot',
    'cauliflower', 'corn', 'cucumber', 'eggplant', 'garlic', 'ginger',
    'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango', 'onion',
    'orange', 'paprika', 'pear', 'peas', 'pepper_bell', 'pepper_chilli',
    'pineapple', 'pomegranate', 'potato', 'raddish', 'spinach', 'sweetcorn',
    'tomato', 'turnip', 'watermelon'
]

INGREDIENTS_COLUMN = "ingredients"
INSTRUCTIONS_COLUMN = "instructions"
TYPES_COLUMN = "types"
NAME_COLUMN = "name"
INGREDIENTS_PARSED_COLUMN = "ingredients_parsed"

DATAFRAME_INIT_COLUMNS = ['cuisine', 'types', 'name', 'ingredients', 'difficulty', "health_banners", 'instructions', 'link']
DROP_DUPLICATES_BY_COLUMN = INGREDIENTS_COLUMN
LIST_PARAMS_PARSED_MODEL = ['cuisine', 'types', 'health_banners', 'ingredients_parsed', 'instructions', 'link']

# BOT
DEFAULT_RECOMMENDATION_OPTION = "default"
TF_IDF_RECOMMENDATION_OPTION = "tf_idf"
W2V_MEAN_RECOMMENDATION_OPTION = "w2v_mean"
W2V_TF_IDF_RECOMMENDATION_OPTION = "w2v_tf_idf"
