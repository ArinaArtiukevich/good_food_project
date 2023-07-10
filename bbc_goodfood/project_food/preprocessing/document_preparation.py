import pandas as pd

from constants import DROP_DUPLICATES_BY_COLUMN

if __name__ == "__main__":
    csv_files = ['/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/copy/join/1_54.csv',
                 '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/copy/join/55_83.csv',
                 '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/copy/join/84_122.csv',
                 '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/copy/join/123_210.csv',
                 '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/copy/join/210_292.csv',
                 '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/copy/join/293-325.csv',
                 '/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/copy/join/326_333.csv'
                 # todo del 3639

                 ]

    combined_data = pd.DataFrame()

    for file in csv_files:
        df = pd.read_csv(file, sep='\t')
        combined_data = combined_data.append(df, ignore_index=True)

    combined_data.to_csv('/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/copy/join/data_goodfood_bbc.csv',
                         sep="\t", index=False)

    df = pd.read_csv('/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/copy/join/data_goodfood_bbc.csv', sep='\t')
    recipe_df = df.copy()
    print(recipe_df.shape)
    recipe_df.sort_values(DROP_DUPLICATES_BY_COLUMN, inplace=True)
    recipe_df.to_csv('/Users/arina/study/ds/project/food_recommendation/bbc_goodfood/project_food/data/copy/join/data_goodfood_bbc.csv',
                         sep="\t", index=False)
    recipe_df.drop_duplicates(subset=DROP_DUPLICATES_BY_COLUMN, keep=False, inplace=True)
    recipe_df.reset_index(drop=True, inplace=True)
    print(recipe_df)