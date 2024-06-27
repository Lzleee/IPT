import json
import pandas as pd
from tqdm import tqdm
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score


with open('Grocery_and_Gourmet_Food_cleaned.json', "r") as f:
    data = f.readlines()
    print("Review loading...")
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
    with open('meta_Grocery_and_Gourmet_Food.jsonl', "r") as f:
        metadata = f.readlines()
        print("Meta loading...")
        metadata = [json.loads(item) for item in tqdm(metadata)]
        df_meta = pd.DataFrame(metadata)
    df_merged = pd.merge(df_merged, df_meta, on='parent_asin', how='left')
    threshold = 19
    df_merged = df_merged[df_merged['asin_count'] > threshold]
    df_merged = df_merged.reset_index()
    df_merged = df_merged.drop(columns=['main_category',"features","description","videos","store","details","bought_together","subtitle","author"])
    print(df_merged.info(verbose=True, show_counts=True))
    print(df_merged.describe())
    attribute_set = set()
    print("Creating category set...")
    for categories in tqdm(df_merged['categories']):
        attribute_set.update(categories)
    user_set = set(df_merged['user_id'])
    df_merged.to_json('df_merged.jsonl', orient='records', lines=True)
    print(len(df_merged))
    print("Category set:")
    print(len(attribute_set))

    # Constructing a dataframe for user-category mapping
    # user_category_df = pd.DataFrame(columns=['user_id'] + list(attribute_set))
    # for row in tqdm(df_merged.iterrows()):
    #     user_id = row[1]['user_id']
    #     categories = row[1]['categories']
    #     if user_id not in user_category_df.index:
    #         user_category_df.loc[user_id, 'user_id'] = user_id
    #         for category in attribute_set:
    #             user_category_df.at[user_id, category] = 0
    #     for category in categories:
    #         user_category_df.at[user_id, category] += 1
    exploded_df = df_merged.explode('categories')

# Create a crosstab which counts the occurrences of each category for each user
    user_category = pd.crosstab(exploded_df['user_id'], exploded_df['categories'])

    # Fill NaN with 0 if any
    user_category = user_category.fillna(0).astype(int)
    user_category = user_category.reset_index()
            
    print("User-Category dataframe:")
    print(user_category.head())
    user_category.to_json('user_category.jsonl', orient='records', lines=True)



    # # Perform DBSCAN clustering on user-category dataframe
    # clustering = DBSCAN(eps=15, min_samples=5).fit(user_category.iloc[:, 1:])

    # # Get the cluster labels
    # cluster_labels = clustering.labels_

    # # Add the cluster labels to the user-category dataframe
    # user_category['cluster_label'] = cluster_labels
    # print("Cluster labels:")
    # len(set(cluster_labels))
    
    # silhouette = silhouette_score(user_category.iloc[:, 1:], cluster_labels)
    # print('Silhouette Score:', silhouette)

    # # Davies-Bouldin Index
    # davies_bouldin = davies_bouldin_score(user_category.iloc[:, 1:], cluster_labels)
    # print('Davies-Bouldin Index:', davies_bouldin)

    # # Calinski-Harabasz Index
    # calinski_harabasz = calinski_harabasz_score(user_category.iloc[:, 1:], cluster_labels)
    # print('Calinski-Harabasz Index:', calinski_harabasz)

    # # Print the resulting user-category dataframe with cluster labels
    # print("User-Category dataframe with cluster labels:")
    # print(user_category.head())

    # # Save the user-category dataframe with cluster labels to a JSON file
    # user_category.to_json('user_category_clustered.jsonl', orient='records', lines=True)