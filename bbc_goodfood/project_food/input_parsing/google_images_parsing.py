import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class ImageScraper:
    def __init__(self, save_folder: str='background_marble_small_dots', search_query: str='background marble dots'):
        self.save_folder = save_folder
        self.search_query = search_query

        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)
        os.makedirs(save_folder, exist_ok=True)

    def scrape_images(self, num_images: int = 50):
        self.driver.get(f'https://www.google.com/search?q={self.search_query}&tbm=isch')
        for _ in range(5):
            self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(2)
        image_elements = self.driver.find_elements(By.CSS_SELECTOR, '.rg_i')
        downloaded_count = 0

        for i, img_element in enumerate(image_elements):
            if downloaded_count >= num_images:
                break
            img_url = img_element.get_attribute('data-src')

            if img_url and img_url.startswith('http'):
                response = requests.get(img_url)
                image_path = os.path.join(self.save_folder, f'image_{downloaded_count + 1}.jpg')
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                downloaded_count += 1
        self.driver.quit()


if __name__ == "__main__":
    save_folder = 'tomatoes'
    search_query = 'one real tomato photo'
    scraper = ImageScraper(save_folder, search_query)
    scraper.scrape_images(num_images=50)
