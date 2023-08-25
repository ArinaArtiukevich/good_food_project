TELEGRAM_CANCEL_COMMAND = "Enter command /cancel to stop the conversation."
GENERAL_INGREDIENTS_QUESTION = "Please, tell me what ingredients you have."
TELEGRAM_PHOTO_START_CONVERSATION = "Please, add photo, so that i process it.\n" + TELEGRAM_CANCEL_COMMAND
TELEGRAM_INPUT = "Hello! " + GENERAL_INGREDIENTS_QUESTION + " I will try to help you.\n" + TELEGRAM_CANCEL_COMMAND
RECIPE_CATEGORY_MESSAGE = "Please, choose category of the recipe. " + TELEGRAM_CANCEL_COMMAND

TELEGRAM_USER_EXAMPLE_SWEET = "cinnamon, sugar, apple"
TELEGRAM_USER_EXAMPLE_VEGETABLE = "pepper, oil, cucumber"
AVAILABLE_RECIPE_CATEGORY = [
    'lunch', 'soup', 'canapes', 'drink', 'afternoon-tea', 'breads',
    'vegetable', 'breakfast', 'brunch', 'treat', 'cheese-course', 'side-dish',
    'dinner', 'pasta', 'buffet', 'side', 'snack', 'main-course', 'cocktails', 'condiment',
    'starter', 'dessert', 'supper', 'fish-course', 'picnic'
]

MIN_RECIPE_CATEGORY = [
    'vegetable', 'treat', 'main-course',
    'cocktails', 'condiment', 'dessert'
]

DEFAULT_RECOMMENDATION_OPTION = "default"
TF_IDF_RECOMMENDATION_OPTION = "tf_idf"
W2V_MEAN_RECOMMENDATION_OPTION = "w2v_mean"
W2V_TF_IDF_RECOMMENDATION_OPTION = "w2v_tf_idf"
D2V_RECOMMENDATION_OPTION = "doc2vec"
USER_INPUT_CATEGORY = "category"

INGREDIENTS_FIELD = "user_ingredients"

INGREDIENTS_RECOGNITION_ON_PHOTO = "recognition"
MULTIPLE_INGREDIENTS_ON_PHOTO = "multiple"
SINGLE_INGREDIENT_ON_PHOTO = "single"
