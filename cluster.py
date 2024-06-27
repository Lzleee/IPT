import pandas as pd
import json
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from tqdm import tqdm

user_category = pd.read_json('user_category.jsonl', lines=True)
# Perform DBSCAN clustering on user-category dataframe


# # Initialize an empty list to store the sum of squared distances
# ssd = []

# # Iterate over different values of k
# for k in tqdm(range(1, 2000)):
#     # Perform KMeans clustering with current k value
#     clustering = KMeans(n_clusters=k, init='k-means++').fit(user_category.iloc[:, 1:])
    
#     # Calculate the sum of squared distances
#     ssd.append(clustering.inertia_)

# # Plot the elbow diagram
# plt.plot(range(1, 2000), ssd, marker='o')
# plt.xlabel('Number of Clusters (k)')
# plt.ylabel('Sum of Squared Distances')
# plt.title('Elbow Diagram')
# plt.savefig('/home/lizhili/DataMining/elbow_diagram.png')

clustering = KMeans(n_clusters=2000, init='k-means++').fit(user_category.iloc[:, 1:])
# Get the cluster labels
cluster_labels = clustering.labels_

# Add the cluster labels to the user-category dataframe
user_category['cluster_label'] = cluster_labels
print("Cluster labels:")
print(len(set(cluster_labels)))

silhouette = silhouette_score(user_category.iloc[:, 1:], cluster_labels)
print('Silhouette Score:', silhouette)

# Davies-Bouldin Index
davies_bouldin = davies_bouldin_score(user_category.iloc[:, 1:], cluster_labels)
print('Davies-Bouldin Index:', davies_bouldin)

# Calinski-Harabasz Index
calinski_harabasz = calinski_harabasz_score(user_category.iloc[:, 1:], cluster_labels)
print('Calinski-Harabasz Index:', calinski_harabasz)

# Print the resulting user-category dataframe with cluster labels
print("User-Category dataframe with cluster labels:")
print(user_category.head())

user_label = user_category[['user_id', 'cluster_label']]

# Save the user-category dataframe with cluster labels to a JSON file
user_label.to_json('user_category_clustered2.jsonl', orient='records', lines=True)