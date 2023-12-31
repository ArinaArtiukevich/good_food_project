import json
import math
import sys
from abc import ABC, abstractmethod
from typing import List

import bs4
import joblib
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append("..")
from configs.constants import DATA_PATH_FULL_PICKLE, DATAFRAME_INIT_COLUMNS
from data.schema.recipe import ExtendedRecipeModel


class RecipeParser(ABC):
    @abstractmethod
    def parse_recipes(self):
        pass


class BBCRecipesParses(RecipeParser):
    URL = 'https://www.bbcgoodfood.com/search?tab=recipe'
    BASIC_URL = 'https://www.bbcgoodfood.com/recipes'
    EXPECTED_NUMBER_OF_RECIPIES = 10_000
    MEAL_TYPE = "?mealType="
    PAGE_PARAM = "&page="

    def __init__(self, driver: webdriver = None):
        self.driver = driver if driver is not None else webdriver.Chrome(
            service=Service(ChromeDriverManager(version="114.0.5735.90").install()))

    def parse_recipes(self, url: str = URL, return_dataframe: bool = True) -> List[ExtendedRecipeModel] | pd.DataFrame:
        input_recipes = pd.DataFrame(columns=DATAFRAME_INIT_COLUMNS) if return_dataframe else []
        pages = math.ceil(self.EXPECTED_NUMBER_OF_RECIPIES / 30)
        for page in range(1, pages):
            current_url = url + self.PAGE_PARAM + str(page)
            print(current_url)
            temp = self.generate_dataset(url=current_url, return_dataframe=return_dataframe)
            input_recipes = input_recipes.append(temp) if return_dataframe else input_recipes + temp

        self.driver.close()
        self.driver.quit()
        return input_recipes

    def generate_dataset(self, url: str, basic_url: str = BASIC_URL, return_dataframe: bool = True) -> List[
                                                                                                           ExtendedRecipeModel] | pd.DataFrame:
        result = pd.DataFrame(columns=DATAFRAME_INIT_COLUMNS) if return_dataframe else []
        articles = self.get_all_articles(url)
        for article in articles:
            recipe_url = article.find('a').get('href')
            recipe_title = article.find('h2', attrs={'class': 'heading-4'}).getText()
            recipe_request = ""
            while recipe_request == "":
                try:
                    recipe_request = requests.get(basic_url + recipe_url)
                    break
                except requests.exceptions.ConnectionError:
                    print(f"Could not get {basic_url + recipe_url}")
                    continue
            recipe_parser = bs4.BeautifulSoup(recipe_request.text, features="html.parser")
            try:
                parsed_recipe = self.get_recipes_from_page(recipe_parser, recipe_title)
                if return_dataframe:
                    result.loc[len(result)] = [
                        parsed_recipe.cuisine,
                        parsed_recipe.types,
                        parsed_recipe.name,
                        parsed_recipe.ingredients,
                        parsed_recipe.difficulty,
                        parsed_recipe.health_banners,
                        parsed_recipe.instructions,
                        parsed_recipe.link
                    ]
                else:
                    result.append(parsed_recipe)
            except:
                print("Could not find an item during scrapping. Ignore this page")
        return result

    def get_recipes_from_page(self, recipe_parser: bs4.BeautifulSoup, recipe_title: str) -> ExtendedRecipeModel:
        tags = json.loads(
            recipe_parser.find('script', attrs={'type': 'application/json', 'id': "__AD_SETTINGS__"})
            .contents[0])['targets']
        ingredients_space = recipe_parser.find('section', attrs={'class': 'recipe__ingredients'})
        planner_space = recipe_parser.find('ul', attrs={'class': 'post-header__planning'})
        health_banners_space = recipe_parser.find('ul', attrs={'class': 'post-header__term-icons-list'})
        instructions_space = recipe_parser.find('section', attrs={'class': 'recipe__method-steps'})

        current_link = recipe_parser.find('link', attrs={'data-testid': "meta-canonical"}).get('href')
        ingredients = self.get_ingredients(ingredients_space)
        planner_soup = planner_space.find('div', attrs={'class': 'post-header__skill-level'})
        health_banners = self.get_health_banners(health_banners_space)
        instructions = self.get_instructions(instructions_space)

        recipe = ExtendedRecipeModel(
            cuisine=tags['cuisine'] if 'cuisine' in tags else None,
            types=tags['meal-type'] if 'meal-type' in tags else None,
            name=recipe_title,
            ingredients=str(ingredients),
            difficulty=planner_soup.getText(),
            health_banners=health_banners,
            instructions=str(instructions),
            link=current_link
        )
        return recipe

    def get_all_articles(self, url: str):
        self.driver.get(url)
        elem = self.driver.find_element(By.CLASS_NAME, 'load-more-paginator__btn')
        self.driver.execute_script("arguments[0].click();", elem)
        driver_parser = bs4.BeautifulSoup(self.driver.page_source, features="html.parser")
        parsed_articles = driver_parser.find_all('article', attrs={
            'class': 'card text-align-left card--horizontal card--inline card--with-borders'})
        return parsed_articles

    def get_instructions(self, instructions_space: bs4.Tag):
        instructions = []
        try:
            instructions_soup = instructions_space.find_all('div', attrs={
                'class': 'editor-content'})
            for instruction in range(len(instructions_soup)):
                instructions.append(instructions_soup[instruction].getText())
        except AttributeError:
            print("Could not find an item during scrapping. Ignore this page")
        return instructions

    def get_ingredients(self, ingredients_space: bs4.Tag):
        ingredients = []
        try:
            ingredients_soup = ingredients_space.find_all('li', attrs={
                'class': 'pb-xxs pt-xxs list-item list-item--separator'})
            for ingredient in range(len(ingredients_soup)):
                ingredients.append(ingredients_soup[ingredient].getText())
        except AttributeError:
            print("Could not find an item during scrapping. Ignore this page")
        return ingredients

    def get_health_banners(self, health_banners_space: bs4.Tag):
        health_banners = []
        try:
            health_banners_soup = health_banners_space.find_all('li', attrs={'class': 'list-item'})
            for health_banner in range(len(health_banners_soup)):
                health_banners.append(health_banners_soup[health_banner].getText())
        except AttributeError:
            print("Could not find an item during scrapping. Ignore this page")
        return health_banners


if __name__ == "__main__":
    parser = BBCRecipesParses()

    # PICKLE
    data = parser.parse_recipes(return_dataframe=False)
    joblib.dump(data, DATA_PATH_FULL_PICKLE)
    data = joblib.load(DATA_PATH_FULL_PICKLE)

    # CSV FILE
    # data = parser.parse_recipes(return_dataframe=True)
    # df = pd.DataFrame(data)
    # df.to_csv(
    #     DATA_CSV_PATH_FULL_CSV,
    #     sep="\t", index=False)
