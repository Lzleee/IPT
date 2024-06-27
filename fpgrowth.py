import pandas as pd
import json
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from tqdm import tqdm
import json

item_list = []
with open("user_and_product_level20.jsonl", "r") as file:
    lines = file.readlines()
    item_list = [json.loads(item)["products"] for item in tqdm(lines)]
te = TransactionEncoder()
df_tf = te.fit_transform(item_list)
df = pd.DataFrame(df_tf,columns=te.columns_)
print("Calculating frequent itemsets...")
frequent_itemsets = fpgrowth(df, min_support=0.0003, use_colnames=True, verbose=1)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
rules.sort_values(by='confidence',ascending=False, inplace=True)
frequent_itemsets.sort_values(by='support',ascending=False, inplace=True)
frequent_itemsets = frequent_itemsets[frequent_itemsets['itemsets'].apply(lambda x: len(x) > 1)]
frequent_itemsets.to_json('frequent_itemsets.jsonl', orient='records', lines=True)
rules.to_json('rules.jsonl', orient='records', lines=True)
with open("meta_Grocery_and_Gourmet_Food.jsonl", "r") as file:
    data = file.readlines()
    print("Meta data loading...")
    data = [json.loads(item) for item in tqdm(data)]
    df_meta = pd.DataFrame(data)
    with open("frequent_itemsets.jsonl", "r") as file:
        data = file.readlines()
        print("Frequent itemsets loading...")
        data = [json.loads(item) for item in tqdm(data)]
        for item in data:
            item["itemsets"] = list(item["itemsets"])
        print("Replacing...")
        with open("frequent_itemsets_items.jsonl", "w") as file:
            file.write("")
        with open("frequent_itemsets_items.jsonl", "a") as file:
            for item in tqdm(data):
                for i in range(len(item["itemsets"])):
                    item["itemsets"][i] = df_meta[df_meta['parent_asin'] == item["itemsets"][i]]['title'].values[0]
                file.write(json.dumps(item) + "\n")
    
    with open("rules.jsonl", "r") as file:
        data = file.readlines()
        print("Rules loading...")
        data = [json.loads(item) for item in tqdm(data)]
        for item in data:
            item["antecedents"] = list(item["antecedents"])
            item["consequents"] = list(item["consequents"])
        print("Replacing...")
        with open("rules_items.jsonl", "w") as file:
            file.write("")
        with open("rules_items.jsonl", "a") as file:
            for item in tqdm(data):
                for i in range(len(item["antecedents"])):
                    item["antecedents"][i] = df_meta[df_meta['parent_asin'] == item["antecedents"][i]]['title'].values[0]
                for i in range(len(item["consequents"])):
                    item["consequents"][i] = df_meta[df_meta['parent_asin'] == item["consequents"][i]]['title'].values[0]
                file.write(json.dumps(item) + "\n")
        
            