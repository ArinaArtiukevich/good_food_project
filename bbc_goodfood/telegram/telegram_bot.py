import ast
import json
from typing import Tuple, List, Any

import pandas as pd
import requests
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters, ConversationHandler
import sys

sys.path.append("..")
from configs.dev import BOT_TOKEN, FAST_API_RECOMMENDER_URL
from configs.constants import TELEGRAM_INPUT, DEFAULT_RECOMMENDATION_OPTION, \
    TF_IDF_RECOMMENDATION_OPTION, W2V_MEAN_RECOMMENDATION_OPTION, W2V_TF_IDF_RECOMMENDATION_OPTION, \
    TELEGRAM_USER_EXAMPLE_VEGETABLE, TELEGRAM_USER_EXAMPLE_SWEET

RECIPE_RECOMMENDER = 0
keyboard = [[TELEGRAM_USER_EXAMPLE_VEGETABLE, TELEGRAM_USER_EXAMPLE_SWEET]]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! What ingredients do you have?')


async def parse_preprocess_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = FAST_API_RECOMMENDER_URL + "/parse"
    df = pd.DataFrame(requests.get(request))
    request = FAST_API_RECOMMENDER_URL + '/preprocess'
    df = pd.DataFrame(requests.get(request))
    await update.message.reply_text('Recipes were successfully parsed and preprocessed.')


async def recipe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[DEFAULT_RECOMMENDATION_OPTION] = 1
    await update.message.reply_text(
        TELEGRAM_INPUT,
        reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True
        )
    )
    return RECIPE_RECOMMENDER


async def tf_idf_recipe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[TF_IDF_RECOMMENDATION_OPTION] = 1
    await update.message.reply_text(
        TELEGRAM_INPUT,
        reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True
        )
    )
    return RECIPE_RECOMMENDER


async def w2v_mean_recipe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[W2V_MEAN_RECOMMENDATION_OPTION] = 1
    await update.message.reply_text(
        TELEGRAM_INPUT,
        reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True
        )
    )
    return RECIPE_RECOMMENDER


async def w2v_tf_idf_recipe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[W2V_TF_IDF_RECOMMENDATION_OPTION] = 1
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
    elif context.user_data[TF_IDF_RECOMMENDATION_OPTION]:
        request = request + TF_IDF_RECOMMENDATION_OPTION
    elif context.user_data[W2V_MEAN_RECOMMENDATION_OPTION]:
        request = request + W2V_MEAN_RECOMMENDATION_OPTION
    else:
        await update.message.reply_text(
            "Something went wrong. Please, try again later.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    ingredients_input = update.message.text
    result_list = ingredients_input.split(", ")
    if len(result_list) <= 1:
        await update.message.reply_text(
            "Incorrect input. Please, try again later.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    params = {
        'user_input': result_list
    }
    response = requests.get(request, params)
    json_response = json.loads(response.content)

    result_output = ''
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


def get_output(input_dict: dict) -> str:
    list_input_keys = list(input_dict.keys())
    parsed_name_ingredients = parse_name_ingredients(list_input_keys)
    initial_output = "Based on the ingredients we recommend you to choose from: \n\n"
    result = "".join(name + ingredients + '\n' for (name, ingredients) in parsed_name_ingredients)
    return initial_output + result


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


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


#
# def handle_response(text: str) -> str:
#     # Create your own response logic
#     processed: str = text.lower()
#
#     if 'hello' in processed:
#         return 'Hey there!'
#
#     if 'how are you' in processed:
#         return 'I\'m good!'
#
#     if 'i love python' in processed:
#         return 'Remember to subscribe!'
#
#     return 'I don\'t understand'
#
#
# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message_type: str = update.message.chat.type
#     text: str = update.message.text
#
#     print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
#
#     response: str = handle_response(text)
#     await update.message.reply_text(response)
#

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('parse', parse_preprocess_command))

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('recipe', recipe_command),
            CommandHandler('tf_idf_recipe', tf_idf_recipe_command),
            CommandHandler('w2v_mean_recipe', w2v_mean_recipe_command),
            CommandHandler('w2v_tf_idf_recipe', w2v_tf_idf_recipe_command)
        ],
        states={
            RECIPE_RECOMMENDER: [MessageHandler(filters.TEXT, recipe_recommender_command)]
        },
        fallbacks=[CommandHandler('cancel', cancel_command)],
    )
    app.add_handler(conv_handler)

    # Messages
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=3)
