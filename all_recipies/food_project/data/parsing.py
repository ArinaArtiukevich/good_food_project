from abc import ABC, abstractmethod
import bs4
import pandas as pd
import requests


class RecipeParser(ABC):
    @abstractmethod
    def parse_category_links(self):
        pass

    @abstractmethod
    def parse_recipes(self):
        pass


class AllRecipesParses(RecipeParser):
    CATEGORY_URL = 'https://www.allrecipes.com/recipes-a-z-6735880'

    def parse_category_links(self, search_url: str = CATEGORY_URL) -> pd.DataFrame:
        page = ""
        try:
            page = requests.get(search_url)
        except requests.exceptions.ConnectionError:
            print("Connection problems")
            # TODO
        parser = bs4.BeautifulSoup(page.text)
        meal_categories = parser.find('ul', attrs={'class': 'link-list'})
        categories = pd.DataFrame(columns=['type', 'url', 'number'])
        # for link in meal_categories.find_all('li'):
        #     val = link.select_one('input')['value']
        #     categories.loc[len(categories)] = [val, seacrh_url + search_type + val,
        #                                        int(re.findall(r'\d+', link.getText())[0])]
        # categories.to_csv(
        #     r"/Users/arina/study/ds/project/food_recommendation/input/bcc_goodfood/categories_links_bbc.csv", sep="\t",
        #     index=False)
        return None

    def parse_recipes(self):
        pass


AllRecipesParses().parse_category_links()