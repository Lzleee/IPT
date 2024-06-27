import pandas as pd
import json
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth
from tqdm import tqdm



with open('Grocery_and_Gourmet_Food_cleaned.json', "r") as f:
    data = f.readlines()
    print("loading...")
    data = [json.loads(item) for item in tqdm(data)]
    df = pd.DataFrame(data)
    print(df.info(verbose=True, show_counts=True))
    print(df.describe())
    unique_user_ids = df['user_id'].nunique()
    unique_product_ids = df['parent_asin'].nunique()
    print("Number of unique user IDs:", unique_user_ids)
    print("Number of unique product IDs:", unique_product_ids)
    user_item_counts = df.groupby('user_id')['parent_asin'].count()
    user_item_counts = pd.DataFrame(user_item_counts).reset_index()
    user_item_counts = user_item_counts.rename(columns={'parent_asin': 'asin_count'})
    df_merged = pd.merge(df, user_item_counts, on='user_id', how='left')
    print(df_merged.describe())
    threshold = 19
    df_merged = df_merged[df_merged['asin_count'] > threshold]
    df_merged = df_merged.reset_index()
    result_path = f"user_and_product_level{threshold+1}.jsonl"
    with open(result_path, "w") as file:
        file.write("")
    with open(result_path,"a") as file:
        print("Creating item dictionary...")
        temp={}
        for index, row in tqdm(df_merged.iterrows()):
            user_id = row["user_id"]
            if index == 0:
                temp["products"]=[]
                temp["user_id"]=user_id
                continue
            if temp["user_id"] != user_id:
                file.write(json.dumps(temp) + "\n")
                temp["products"]=[]
                temp["user_id"]=user_id
            temp["products"].append(row["parent_asin"])
        file.write(json.dumps(temp) + "\n")
    # item_list = list(itemDict.values())
    # te = TransactionEncoder()
    # df_tf = te.fit_transform(item_list)
    # df = pd.DataFrame(df_tf,columns=te.columns_)
    # print("Calculating frequent itemsets...")
    # frequent_itemsets = fpgrowth(df, min_support=0.001, use_colnames=True)
    # frequent_itemsets.sort_values(by='support',ascending=False, inplace=True)
    # with open('frequent_itemsets.txt', "w") as file:
    #     file.write(frequent_itemsets.to_string())