import ast
import json
import os
import sys
import pandas as pd
import requests

from typing import List
from starlette import status
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters, ConversationHandler
import sys

sys.path.append("..")
# from configs.dev import BOT_TOKEN, FAST_API_RECOMMENDER_URL
from configs.constants import TELEGRAM_INPUT, DEFAULT_RECOMMENDATION_OPTION, \
    TF_IDF_RECOMMENDATION_OPTION, W2V_MEAN_RECOMMENDATION_OPTION, W2V_TF_IDF_RECOMMENDATION_OPTION, \
    TELEGRAM_USER_EXAMPLE_VEGETABLE, TELEGRAM_USER_EXAMPLE_SWEET, TELEGRAM_PHOTO_START_CONVERSATION, INGREDIENTS_FIELD, \
    D2V_RECOMMENDATION_OPTION, MIN_RECIPE_CATEGORY, AVAILABLE_RECIPE_CATEGORY, RECIPE_CATEGORY_MESSAGE, \
    GENERAL_INGREDIENTS_QUESTION, USER_INPUT_CATEGORY, MULTIPLE_INGREDIENTS_ON_PHOTO, SINGLE_INGREDIENT_ON_PHOTO, \
    INGREDIENTS_RECOGNITION_ON_PHOTO

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')
FAST_API_RECOMMENDER_URL = os.getenv('FAST_API_RECOMMENDER_URL')
FAST_API_TELEGRAM_URL = os.getenv('FAST_API_TELEGRAM_URL')

RECIPE_RECOMMENDER = 0
PHOTO_2_INGREDIENTS = 1
PHOTO_RECIPE_RECOMMENDER = 2

ADVICE_OPTION = 3
CHOOSE_CATEGORY = 4

keyboard = [[TELEGRAM_USER_EXAMPLE_VEGETABLE, TELEGRAM_USER_EXAMPLE_SWEET]]
categories = [MIN_RECIPE_CATEGORY]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! What ingredients do you have?')


async def parse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = FAST_API_RECOMMENDER_URL + '/data/parse/csv'
    df = pd.DataFrame(requests.get(request))
    await update.message.reply_text('Recipes were successfully parsed.')


async def preprocess_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = FAST_API_RECOMMENDER_URL + '/data/preprocess/csv'
    df = pd.DataFrame(requests.get(request))
    await update.message.reply_text('Recipes were successfully preprocessed.')


async def train_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Server error. Please, try again later."
    try:
        request = FAST_API_RECOMMENDER_URL + '/recipe/train/'

        response_tf_idf = requests.get(request + TF_IDF_RECOMMENDATION_OPTION)
        response_w2v_mean = requests.get(request + W2V_MEAN_RECOMMENDATION_OPTION)
        response_w2v_tf_idf = requests.get(request + W2V_TF_IDF_RECOMMENDATION_OPTION)
        response_d2v = requests.get(request + D2V_RECOMMENDATION_OPTION)

        if response_tf_idf.content is status.HTTP_201_CREATED and \
                response_w2v_mean.content is status.HTTP_201_CREATED and \
                response_w2v_tf_idf.content is status.HTTP_201_CREATED and \
                response_d2v.content is status.HTTP_201_CREATED:
            message = 'Models were successfully trained.'

    except Exception:
        await update.message.reply_text(
            message,
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    await update.message.reply_text('Models were successfully trained.')
    return ConversationHandler.END


async def advice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        RECIPE_CATEGORY_MESSAGE,
        reply_markup=ReplyKeyboardMarkup(
            categories, one_time_keyboard=True
        )
    )
    return CHOOSE_CATEGORY


async def choose_category_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_category = update.message.text.lower()
    if user_category not in AVAILABLE_RECIPE_CATEGORY:
        await update.message.reply_text(
            "No such category. Please, try again later.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    context.user_data[USER_INPUT_CATEGORY] = user_category
    await update.message.reply_text(
        GENERAL_INGREDIENTS_QUESTION,
        reply_markup=ReplyKeyboardRemove()
    )
    return PHOTO_RECIPE_RECOMMENDER


async def recipe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[DEFAULT_RECOMMENDATION_OPTION] = 1
    context.user_data[TF_IDF_RECOMMENDATION_OPTION] = 0
    context.user_data[W2V_TF_IDF_RECOMMENDATION_OPTION] = 0
    context.user_data[W2V_MEAN_RECOMMENDATION_OPTION] = 0
    context.user_data[D2V_RECOMMENDATION_OPTION] = 0
    await update.message.reply_text(
        TELEGRAM_INPUT,
        reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True
        )
    )
    return RECIPE_RECOMMENDER


async def tf_idf_recipe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[DEFAULT_RECOMMENDATION_OPTION] = 0
    context.user_data[TF_IDF_RECOMMENDATION_OPTION] = 1
    context.user_data[W2V_TF_IDF_RECOMMENDATION_OPTION] = 0
    context.user_data[W2V_MEAN_RECOMMENDATION_OPTION] = 0
    context.user_data[D2V_RECOMMENDATION_OPTION] = 0
    await update.message.reply_text(
        TELEGRAM_INPUT,
        reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True
        )
    )
    return RECIPE_RECOMMENDER


async def w2v_mean_recipe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[DEFAULT_RECOMMENDATION_OPTION] = 0
    context.user_data[TF_IDF_RECOMMENDATION_OPTION] = 0
    context.user_data[W2V_TF_IDF_RECOMMENDATION_OPTION] = 0
    context.user_data[W2V_MEAN_RECOMMENDATION_OPTION] = 1
    context.user_data[D2V_RECOMMENDATION_OPTION] = 0
    await update.message.reply_text(
        TELEGRAM_INPUT,
        reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True
        )
    )
    return RECIPE_RECOMMENDER


async def w2v_tf_idf_recipe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[DEFAULT_RECOMMENDATION_OPTION] = 0
    context.user_data[TF_IDF_RECOMMENDATION_OPTION] = 0
    context.user_data[W2V_TF_IDF_RECOMMENDATION_OPTION] = 1
    context.user_data[W2V_MEAN_RECOMMENDATION_OPTION] = 0
    context.user_data[D2V_RECOMMENDATION_OPTION] = 0
    await update.message.reply_text(
        TELEGRAM_INPUT,
        reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True
        )
    )
    return RECIPE_RECOMMENDER


async def doc2vec_recipe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[DEFAULT_RECOMMENDATION_OPTION] = 0
    context.user_data[TF_IDF_RECOMMENDATION_OPTION] = 0
    context.user_data[W2V_TF_IDF_RECOMMENDATION_OPTION] = 0
    context.user_data[W2V_MEAN_RECOMMENDATION_OPTION] = 0
    context.user_data[D2V_RECOMMENDATION_OPTION] = 1
    await update.message.reply_text(
        TELEGRAM_INPUT,
        reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True
        )
    )
    return RECIPE_RECOMMENDER


async def recipe_recommender_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "The request is in process. Please, wait.",
        reply_markup=ReplyKeyboardRemove()
    )
    request = FAST_API_RECOMMENDER_URL + "/recipe/"
    if context.user_data[DEFAULT_RECOMMENDATION_OPTION] or context.user_data[W2V_TF_IDF_RECOMMENDATION_OPTION]:
        request = request + W2V_TF_IDF_RECOMMENDATION_OPTION
        context.user_data[DEFAULT_RECOMMENDATION_OPTION] = 0
        context.user_data[W2V_TF_IDF_RECOMMENDATION_OPTION] = 0
    elif context.user_data[TF_IDF_RECOMMENDATION_OPTION]:
        request = request + TF_IDF_RECOMMENDATION_OPTION
        context.user_data[TF_IDF_RECOMMENDATION_OPTION] = 0
    elif context.user_data[W2V_MEAN_RECOMMENDATION_OPTION]:
        request = request + W2V_MEAN_RECOMMENDATION_OPTION
        context.user_data[W2V_MEAN_RECOMMENDATION_OPTION] = 0
    elif context.user_data[D2V_RECOMMENDATION_OPTION]:
        request = request + D2V_RECOMMENDATION_OPTION
        context.user_data[D2V_RECOMMENDATION_OPTION] = 0
    else:
        await update.message.reply_text(
            "Something went wrong. Please, try again later.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    try:
        ingredients_input = preprocess_user_input(update.message.text)
    except ValueError as err:
        await update.message.reply_text(
            str(err),
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    params = {
        'user_input': ingredients_input
    }
    response = requests.get(request, params)
    json_response = json.loads(response.content)
    try:
        result_output = get_output(json_response)
    except json.JSONDecodeError:
        await update.message.reply_text(
            "Server error. Please, try again later.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    await update.message.reply_text(
        result_output
    )
    return ConversationHandler.END


def preprocess_user_input(ingredients_input: str | List[str]) -> List[str]:
    result_list = ingredients_input.split(", ") if isinstance(ingredients_input, str) else ingredients_input
    if len(result_list) == 1 and result_list[0] == "no":
        raise ValueError("Please, enter several ingredients divided by coma.")
    return result_list


def get_output(input_dict: dict) -> str:
    list_input_keys = list(input_dict.keys())
    parsed_name_ingredients = parse_name_ingredients(list_input_keys)
    initial_output = "Based on the ingredients we recommend you to choose from: \n\n"
    result = "".join(name + ingredients + '\n' for (name, ingredients) in parsed_name_ingredients)
    end_output = "\n\n Please, visit https://www.bbcgoodfood.com/ to see more details."
    return initial_output + result + end_output


def parse_name_ingredients(input_result: List[str]) -> list[tuple[str, str]]:
    list_name_ingredients = [ast.literal_eval(value) for value in input_result]
    return [(name, prettify_output(ingredients)) for (name, ingredients) in list_name_ingredients]


def prettify_output(input_string: str) -> str:
    ingredients_list = ast.literal_eval(input_string)
    ingredients_string = '\n'.join('\t' + ingredient for ingredient in ingredients_list)
    return '\n' + ingredients_string + '\n'


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'The operation canceled.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def process_photo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[INGREDIENTS_RECOGNITION_ON_PHOTO] = SINGLE_INGREDIENT_ON_PHOTO
    await update.message.reply_text(
        TELEGRAM_PHOTO_START_CONVERSATION,
        reply_markup=ReplyKeyboardRemove()
    )
    return PHOTO_2_INGREDIENTS


async def process_mult_ingredients_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[INGREDIENTS_RECOGNITION_ON_PHOTO] = MULTIPLE_INGREDIENTS_ON_PHOTO
    await update.message.reply_text(
        TELEGRAM_PHOTO_START_CONVERSATION,
        reply_markup=ReplyKeyboardRemove()
    )
    return PHOTO_2_INGREDIENTS


async def photo2ingredients_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    file_id = update.message.photo[-1].file_id
    img_file = await context.bot.get_file(file_id)
    image_data = await img_file.download_as_bytearray()
    request = FAST_API_RECOMMENDER_URL
    if INGREDIENTS_RECOGNITION_ON_PHOTO in context.user_data:
        request += '/photo2multiple_ingredients' if context.user_data[INGREDIENTS_RECOGNITION_ON_PHOTO] == MULTIPLE_INGREDIENTS_ON_PHOTO else '/photo2ingredients'
        context.user_data[INGREDIENTS_RECOGNITION_ON_PHOTO] = None
    else:
        request += '/photo2ingredients'

    files = [
        ("image", (f"{user_id}_{file_id}.jpg", image_data, "image/jpg"))
    ]
    await update.message.reply_text(
        'The photo is being processed. Please, wait.',
        reply_markup=ReplyKeyboardRemove()
    )
    response = requests.post(request, files=files)
    context.user_data[INGREDIENTS_FIELD] = ast.literal_eval(response.text)
    result_response = ', '.join(ast.literal_eval(response.text))
    if result_response:
        bot_response = f'I found {result_response} on the photo. Is it correct? Please, confirm or type the ingredients.'
    else:
        bot_response = 'I am sorry, I could not find any ingredient on the photo. If you want to find recipes, ' \
                       'please enter the ingredients.'
    await update.message.reply_text(
        bot_response,
        reply_markup=ReplyKeyboardRemove()
    )
    return PHOTO_RECIPE_RECOMMENDER


async def general_recipe_recommender_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_response = update.message.text
    if user_response.lower() != 'yes':
        context.user_data[INGREDIENTS_FIELD] = user_response
    request = FAST_API_RECOMMENDER_URL + "/recipe/" + D2V_RECOMMENDATION_OPTION
    try:
        ingredients_input = preprocess_user_input(context.user_data[INGREDIENTS_FIELD])
        context.user_data[INGREDIENTS_FIELD] = None
    except ValueError as err:
        await update.message.reply_text(
            str(err),
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    if USER_INPUT_CATEGORY in context.user_data:
        request += "/category"
        params = {
            USER_INPUT_CATEGORY: context.user_data[USER_INPUT_CATEGORY],
            'user_input': ingredients_input
        }
        context.user_data[USER_INPUT_CATEGORY] = None
    else:
        params = {
            'user_input': ingredients_input
        }

    response = requests.get(request, params)
    json_response = json.loads(response.content)
    try:
        result_output = get_output(json_response)
    except json.JSONDecodeError:
        await update.message.reply_text(
            "Server error. Please, try again later.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    await update.message.reply_text(
        result_output
    )
    return ConversationHandler.END


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


def handle_response(text: str) -> str:
    try:
        ingredients_input = preprocess_user_input(text)
    except ValueError as err:
        result_output = str(err)
        return result_output
    params = {
        'user_input': ingredients_input
    }
    response = requests.get(FAST_API_RECOMMENDER_URL + '/recipe/' + W2V_TF_IDF_RECOMMENDATION_OPTION, params)
    json_response = json.loads(response.content)
    try:
        result_output = get_output(json_response)
    except json.JSONDecodeError:
        return "Server error. Please, try again later."
    return result_output


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    response = handle_response(text)
    await update.message.reply_text(response)


if __name__ == '__main__':
    print(BOT_TOKEN)
    app = Application.builder().token(token='6421904425:AAH22gBs6bGYVZ2XekeO5yqmReXkJMyS3n0').build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('parse', parse_command))
    app.add_handler(CommandHandler('preprocess', preprocess_command))
    app.add_handler(CommandHandler('train', train_command))

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('recipe', recipe_command),
            CommandHandler('tf_idf_recipe', tf_idf_recipe_command),
            CommandHandler('w2v_mean_recipe', w2v_mean_recipe_command),
            CommandHandler('w2v_tf_idf_recipe', w2v_tf_idf_recipe_command),
            CommandHandler('doc2vec_recipe', doc2vec_recipe_command)
        ],
        states={
            RECIPE_RECOMMENDER: [MessageHandler(filters.TEXT, recipe_recommender_command)]
        },
        fallbacks=[CommandHandler('cancel', cancel_command)],
    )
    app.add_handler(conv_handler)

    # photo2ingredients
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('process_mult_ingredients_photo', process_mult_ingredients_command),
            CommandHandler('process_single_ingredient_photo', process_photo_command)
        ],
        states={
            PHOTO_2_INGREDIENTS: [MessageHandler(filters.PHOTO, photo2ingredients_command)],
            PHOTO_RECIPE_RECOMMENDER: [MessageHandler(filters.TEXT, general_recipe_recommender_command)]
        },
        fallbacks=[CommandHandler('cancel', cancel_command)],
    )
    app.add_handler(conv_handler)

    # recipe by category
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('advice', advice_command)
        ],
        states={
            CHOOSE_CATEGORY: [MessageHandler(filters.TEXT, choose_category_command)],
            PHOTO_RECIPE_RECOMMENDER: [MessageHandler(filters.TEXT, general_recipe_recommender_command)]
        },
        fallbacks=[CommandHandler('cancel', cancel_command)],
    )
    app.add_handler(conv_handler)

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=3)
