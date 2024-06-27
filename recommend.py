import pandas as pd
import json
import argparse
import random

argparser = argparse.ArgumentParser()
argparser.add_argument("--item", type=str, default="", help="Input a product ID to get recommendations for")
argparser.add_argument("--user_id", type=str, default="")
args = argparser.parse_args()
product_id = args.item
user_id = args.user_id
if product_id != "":
    recommendations = []
    with open("rules.jsonl", "r") as file:
        data = file.readlines()
        data = [json.loads(item) for item in data]
        for item in data:
            if product_id in item["antecedents"]:
                recommendations.append(random.choice(item["consequents"]))
    df = pd.read_json('meta_Grocery_and_Gourmet_Food.jsonl', lines=True)
    product = df[df['parent_asin'] == product_id]["title"].values[0]
    recommendation = random.choice(recommendations)
    recommendation = df[df['parent_asin'] == recommendation]["title"].values[0]
    print(f"Because you viewed {product}, you might also like {recommendation}")
if user_id != "":
    df = pd.read_json('user_category_clustered.jsonl', lines=True)

    if user_id not in df['user_id'].values:
        print("User not found! We recommend a random user from a random cluster.")
        recommend_user = df['user_id'].sample(1).values[0]
    else:
        cluster_label = df[df['user_id'] == user_id]['cluster_label'].values[0]
        recommend_user = df[df['cluster_label'] == cluster_label]['user_id'].sample(1).values[0]
    df_transaction = pd.read_json('user_and_product_level20.jsonl', lines=True)
    recommend_product = df_transaction[df_transaction['user_id'] == recommend_user]['products'].values[0]
    recommend_product = random.choice(recommend_product)
    df_product = pd.read_json('meta_Grocery_and_Gourmet_Food.jsonl', lines=True)
    recommend_product_title = df_product[df_product['parent_asin'] == recommend_product]['title'].values[0]
    print(f"Welcome {user_id}! We recommend you {recommend_product_title}.")
if product_id == "" and user_id == "":
    df_rank = pd.read_json('ranks.jsonl', lines=True)
    top_products = df_rank['title'].head(3).tolist()
    print("Here are top 3 products you may like:")
    for title in top_products:
        print(title)