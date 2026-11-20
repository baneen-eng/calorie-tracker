import pandas as pd
import os

print("Reading data files...")
foods = pd.read_csv('data/raw/food.csv')
nutrients = pd.read_csv('data/raw/nutrient.csv')
food_nutrients = pd.read_csv('data/raw/food_nutrient.csv')
food_categories = pd.read_csv('data/raw/food_category.csv')

foods = foods.merge(food_categories, left_on='food_category_id', right_on='id', how='left', suffixes=('', '_cat'))
foods['category'] = foods['description_cat'].fillna('Unknown')

target_nutrients = ['Energy', 'Protein', 'Total lipid (fat)', 'Carbohydrate, by difference', 'Fiber, total dietary', 'Sugars, total including NLEA']
nutrients_filtered = nutrients[nutrients['name'].isin(target_nutrients)]

food_nutrients_filtered = food_nutrients.merge(nutrients_filtered, left_on='nutrient_id', right_on='id', how='inner', suffixes=('', '_nutrient'))

pivot_table = food_nutrients_filtered.pivot_table(index='fdc_id', columns='name', values='amount', aggfunc='mean').reset_index()

result = foods[['fdc_id', 'description', 'category']].merge(pivot_table, on='fdc_id', how='inner')

column_mapping = {
    'Energy': 'energy_kcal',
    'Protein': 'protein_g',
    'Total lipid (fat)': 'fat_g',
    'Carbohydrate, by difference': 'carbs_g',
    'Fiber, total dietary': 'fiber_g',
    'Sugars, total including NLEA': 'sugars_g'
}
result = result.rename(columns=column_mapping)
result = result.dropna(subset=['energy_kcal'])
result = result.head(1380)

os.makedirs('data', exist_ok=True)
result.to_csv('data/foods.csv', index=False)

print(f"Columns: {list(result.columns)}")
print(f"Saved {len(result)} foods to data/foods.csv")

