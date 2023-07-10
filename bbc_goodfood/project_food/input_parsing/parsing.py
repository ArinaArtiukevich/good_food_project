import json
import math
import time

import bs4
import pandas as pd
import requests

from abc import ABC, abstractmethod
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from constants import DATA_CSV_PATH_FULL, DATAFRAME_INIT_COLUMNS


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
        self.driver = driver if driver is not None else webdriver.Chrome(ChromeDriverManager().install())


    def parse_recipes(self, url: str = URL) -> pd.DataFrame:
        data = pd.DataFrame(columns=DATAFRAME_INIT_COLUMNS)
        pages = math.ceil(self.EXPECTED_NUMBER_OF_RECIPIES / 30)
        for page in range(23, pages):
            current_url = url + self.PAGE_PARAM + str(page)
            print(current_url)
            temp = self.generate_dataset(current_url)
            data = data.append(temp)
        # todo del
            data.to_csv(
                DATA_CSV_PATH_FULL,
                sep="\t", index=False)

        self.driver.close()
        self.driver.quit()
        return data

    def generate_dataset(self, url: str, basic_url: str = BASIC_URL) -> pd.DataFrame:
        result = pd.DataFrame(columns=DATAFRAME_INIT_COLUMNS)
        articles = self.get_all_articles(url)

        print(len(articles))
        j = 0
        for article in articles:
            recipe_url = article.find('a').get('href')
            recipe_title = article.find('h2', attrs={'class': 'heading-4'}).getText()
            print(recipe_title)
            recipe_request = ""
            while recipe_request == "":
                try:
                    recipe_request = requests.get(basic_url + recipe_url)
                    break
                except requests.exceptions.ConnectionError:
                    # TODO
                    print("exc")
                    time.sleep(5)
                    continue
            recipe_parser = bs4.BeautifulSoup(recipe_request.text, features="html.parser")
            try:
                tags = json.loads(recipe_parser.find('script', attrs={'type': 'application/json', 'id': "__AD_SETTINGS__"}).contents[0])['targets']
                ingredients_space = recipe_parser.find('section', attrs={'class': 'recipe__ingredients'})
                planner_space = recipe_parser.find('ul', attrs={'class': 'post-header__planning'})
                health_banners_space = recipe_parser.find('ul', attrs={'class': 'post-header__term-icons-list'})

                ingredients = self.get_ingredients(ingredients_space)
                planner_soup = planner_space.find('div', attrs={'class': 'post-header__skill-level'})
                health_banners = self.get_health_banners(health_banners_space)
                j = j + 1
                result.loc[len(result)] = [tags['cuisine'] if 'cuisine' in tags else None, tags['meal-type'] if 'meal-type' in tags else None, recipe_title, ingredients, planner_soup.getText(), health_banners]

            except:
                # TODO
                print("find_all None error thing. Ignore this page")
        return result

    def get_all_articles(self, url: str):
        self.driver.get(url)
        elem = self.driver.find_element(By.CLASS_NAME, 'load-more-paginator__btn')
        self.driver.execute_script("arguments[0].click();", elem)
        driver_parser = bs4.BeautifulSoup(self.driver.page_source, features="html.parser")
        # list = driver_parser.find('div', attrs={'class': 'layout-md-rail__primary'})
        parsed_articles = driver_parser.find_all('article', attrs={
            'class': 'card text-align-left card--horizontal card--inline card--with-borders'})

        # for article in parsed_articles:
        #     recipe_title = article.find('h2', attrs={'class': 'heading-4'}).getText()
        #     print(recipe_title)
        return parsed_articles

    def get_ingredients(self, ingredients_space: bs4.Tag):
        ingredients = []
        try:
            ingredients_soup = ingredients_space.find_all('li', attrs={
                'class': 'pb-xxs pt-xxs list-item list-item--separator'})
            for ingredient in range(len(ingredients_soup)):
                ingredients.append(ingredients_soup[ingredient].getText())
        except AttributeError:
            # TODO find_all - nothing
            ...
        return ingredients

    def get_health_banners(self, health_banners_space: bs4.Tag):
        health_banners = []
        try:
            health_banners_soup = health_banners_space.find_all('li', attrs={'class': 'list-item'})
            for health_banner in range(len(health_banners_soup)):
                health_banners.append(health_banners_soup[health_banner].getText())
        except AttributeError:
            # TODO find_all - nothing
            ...

        return health_banners


if __name__ == "__main__":
    parser = BBCRecipesParses()
    data = parser.parse_recipes()
    data.to_csv(
        DATA_CSV_PATH_FULL,
        sep="\t", index=False)
