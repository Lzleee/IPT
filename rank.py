import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json('Grocery_and_Gourmet_Food_cleaned.json', lines=True)
asin_count = df['parent_asin'].value_counts()
sorted_asin_count = asin_count.sort_values(ascending=False)
df_sorted = pd.DataFrame(sorted_asin_count).reset_index()
df_product = pd.read_json("meta_Grocery_and_Gourmet_Food.jsonl", lines=True)
df_sorted = pd.merge(df_sorted, df_product, left_on='parent_asin', right_on='parent_asin', how='left')
df_sorted['count_zscore'] = (df_sorted['count'] - df_sorted['count'].mean()) / df_sorted['count'].std()
df_sorted['rating_number_zscore'] = (df_sorted['rating_number'] - df_sorted['rating_number'].mean()) / df_sorted['rating_number'].std()
df_sorted['average_rating_zscore'] = (df_sorted['average_rating'] - df_sorted['average_rating'].mean()) / df_sorted['average_rating'].std()
df_sorted['sum_attributes'] = df_sorted['count_zscore'] + df_sorted['rating_number_zscore'] + df_sorted['average_rating_zscore']
df_sorted = df_sorted.sort_values(by='sum_attributes', ascending=False)
df_sorted[["title","sum_attributes"]].to_json('ranks.jsonl', orient='records', lines=True)