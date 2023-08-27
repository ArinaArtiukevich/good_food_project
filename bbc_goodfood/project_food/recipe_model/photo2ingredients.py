import os
import sys
from collections import defaultdict
from typing import List, Dict

import keras
import numpy as np
from PIL.Image import Image
from tensorflow.keras.preprocessing import image

sys.path.append("..")
from configs.constants import MOBILENET_V5_MODEL, IMG_SIZE, SLIDED_IMAGES_PATH, SLIDED_IMAGES_FOLDER, \
    AVAILABLE_INGREDIENT_NAMES


class Photo2Ingredients:
    def __init__(self, model_path: str = MOBILENET_V5_MODEL):
        self.model = keras.models.load_model(model_path)

    def predict_ingredients(self, image_file: Image):
        image_resized = image_file.resize((IMG_SIZE, IMG_SIZE))
        image_array = image.img_to_array(image_resized)
        img_array = np.array([image_array])
        rescaled_img_array = img_array / 255.0
        prediction = self.model.predict(rescaled_img_array)
        predicted_index = np.argmax(prediction)
        predicted_class_name = AVAILABLE_INGREDIENT_NAMES[predicted_index]
        print(predicted_class_name, np.max(prediction))
        return [predicted_class_name]


class Photo2MultipleIngredients:
    def __init__(self, model_path: str = MOBILENET_V5_MODEL, img_path: str = SLIDED_IMAGES_PATH):
        self.model = keras.models.load_model(model_path)
        self.img_path = img_path

    def get_absolute_img_path(self, image_file: Image) -> str:
        existing_files = [file for file in os.listdir(self.img_path) if
                          os.path.isfile(os.path.join(self.img_path, file))]
        image_files = [file for file in existing_files if file.lower().endswith(".jpg")]
        if image_files:
            last_image_number = max([int(file.split("_")[1].split(".")[0]) for file in image_files])
            next_image_number = last_image_number + 1
        else:
            next_image_number = 1
        new_image_name = f"img_{next_image_number}.jpg"
        new_image_path = os.path.join(self.img_path, new_image_name)
        image_file.save(new_image_path)
        return os.path.abspath(new_image_path)

    def slide_image_window(self, image_file: Image) -> List[str]:
        image_file = image_file.resize((300, 300))
        abs_img_path = self.get_absolute_img_path(image_file)
        file_name = abs_img_path.split('/')[-1]
        new_folder_name = file_name[:file_name.rfind('.')]
        slided_paths = []
        image_number = 1
        right = 150
        lower = 150
        for _ in range(49):
            cropped = image_file.crop((right - 150, lower - 150, right, lower))
            new_folder = os.path.join(SLIDED_IMAGES_PATH + SLIDED_IMAGES_FOLDER, new_folder_name)
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            slided_path = os.path.join(new_folder, str(image_number) + "_" + file_name)
            cropped.save(slided_path)
            slided_paths.append(slided_path.encode('utf-8'))
            right += 25
            image_number += 1
            if (image_number - 1) % 7 == 0:
                right = 150
                lower += 25
        return slided_paths

    def predict_all_ingredients(self, slided_paths: List[str]) -> Dict[str, List[float]]:
        ingredients = defaultdict(list)
        for cropped_path in slided_paths:
            img = image.load_img(cropped_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.array([img_array])
            rescaled_img_array = img_array / 255.0
            prediction = self.model.predict(rescaled_img_array)

            predicted_index = np.argmax(prediction)
            predicted_class_name = AVAILABLE_INGREDIENT_NAMES[predicted_index]
            ingredients[predicted_class_name].append(prediction[:, predicted_index][0])

        return ingredients

    def mean_predicted_ingredients(self, ingredients_dict: Dict[str, List[float]]) -> Dict[str, float]:
        modified_ingredients = {key: sum(values) / len(values) for key, values in ingredients_dict.items()}
        return dict(sorted(modified_ingredients.items(), key=lambda item: item[1], reverse=True))

    def ingredients_list(self, threshold: float, mean_ingredients: Dict[str, float]) -> List[str]:
        ingredients_list = []
        for ingredient, proportion in mean_ingredients.items():
            if proportion > threshold:
                ingredients_list.append(ingredient)
            else:
                break
        return ingredients_list

    def predict_ingredients(self, image_file: Image) -> List[str]:
        ingredients = self.predict_all_ingredients(self.slide_image_window(image_file))
        counted_ingredients = self.mean_predicted_ingredients(ingredients)
        result_ingredients = self.ingredients_list(0.7, counted_ingredients)
        return result_ingredients


if __name__ == "__main__":
    p2ingr = Photo2Ingredients()
    img_path = '../data/photo2ingredients/test_images/cucumber.jpeg'
    img = image.load_img(img_path)
    print(p2ingr.predict_ingredients(img))
