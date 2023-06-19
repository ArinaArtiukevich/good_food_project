import math
import re
import time

import bs4
import pandas as pd
import requests

from abc import ABC, abstractmethod
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from constants import CATEGORY_LINKS_PATH, DATA_CSV_PATH


class RecipeParser(ABC):
    @abstractmethod
    def parse_category_links(self):
        pass

    @abstractmethod
    def parse_recipes(self):
        pass


class BBCRecipesParses(RecipeParser):
    URL = 'https://www.bbcgoodfood.com/search?tab=recipe'
    BASIC_URL = 'https://www.bbcgoodfood.com/recipes'
    MEAL_TYPE = "?mealType="

    def __init__(self, driver: webdriver = None):
        self.driver = driver if driver is not None else webdriver.Chrome(ChromeDriverManager().install())
        self.categories: pd.DataFrame = pd.DataFrame([])

    def parse_category_links(self, search_url: str = URL, search_type: str = MEAL_TYPE) -> pd.DataFrame:
        page = ""
        try:
            page = requests.get(search_url)
        except requests.exceptions.ConnectionError:
            print("Connection problems")
            # TODO
        parser = bs4.BeautifulSoup(page.text, features="html.parser")
        meal_categories = parser.find('ul', attrs={'role': "listbox", 'class': 'ma-reset pa-reset'})
        categories = pd.DataFrame(columns=['type', 'url', 'number'])
        for link in meal_categories.find_all('li'):
            val = link.select_one('input')['value']
            categories.loc[len(categories)] = [val, search_url + search_type + val,
                                               int(re.findall(r'\d+', link.getText())[0])]
        categories.to_csv(
            CATEGORY_LINKS_PATH,
            sep="\t", index=False)
        self.categories = categories
        return categories

    def parse_recipes(self):
        data = pd.DataFrame(columns=['type', 'name', 'ingredients', 'difficulty', "health_banners"])

        for i, row in self.categories.iterrows():
            temp = self.generate_dataset(row["type"], row["url"], row["number"])
            data = data.append(temp)
            data.to_csv(
                DATA_CSV_PATH,
                sep="\t", index=False)

        self.driver.close()
        self.driver.quit()

    def generate_dataset(self, type: str, url: str, n_items: int, basic_url: str = BASIC_URL) -> pd.DataFrame:
        result = pd.DataFrame(columns=['type', 'name', 'ingredients', 'difficulty', "health_banners"])

        articles = self.get_all_articles(url, n_items)

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

            ingredients_space = recipe_parser.find('section', attrs={'class': 'recipe__ingredients'})
            planner_space = recipe_parser.find('ul', attrs={'class': 'post-header__planning'})
            health_banners_space = recipe_parser.find('ul', attrs={'class': 'post-header__term-icons-list'})
            try:
                ingredients = self.get_ingredients(ingredients_space)
                planner_soup = planner_space.find('div', attrs={'class': 'post-header__skill-level'})
                health_banners = self.get_health_banners(health_banners_space)
                j = j + 1
                result.loc[len(result)] = [type, recipe_title, ingredients, planner_soup.getText(), health_banners]
            except:
                # TODO
                print("find_all None error thing. Ignore this page")
        return result

    def get_all_articles(self, url: str, n_items: int):
        if n_items > 70:
            n_items = 60
        parsed_articles = ''
        pages = math.ceil(n_items / 30)

        for n_page in range(1, pages):
            if n_page < 2:
                current_url = url
            else:
                current_url = url + "&page=" + str(n_page)
            print(current_url)
            self.driver.get(current_url)
            elem = self.driver.find_element(By.CLASS_NAME, 'load-more-paginator__btn')
            self.driver.execute_script("arguments[0].click();", elem)
            driver_parser = bs4.BeautifulSoup(self.driver.page_source, features="html.parser")
            # list = driver_parser.find('div', attrs={'class': 'layout-md-rail__primary'})
            parsed_articles = driver_parser.find_all('article', attrs={
                'class': 'card text-align-left card--horizontal card--inline card--with-borders'})

        # for article in parsed_articles:
        #     recipe_title = article.find('h2', attrs={'class': 'heading-4'}).getText()
        #     print(recipe_title)
        if parsed_articles == '':
            print("A")
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
    parser.parse_category_links()
    parser.parse_recipes()
