import random

def euclidean_distance(point1, point2):
    return sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2)) ** 0.5

def assign_points_to_clusters(centroids, data):
    clusters = [[] for _ in centroids]
    for point in data:
        shortest_distance = float('inf')
        for i, centroid in enumerate(centroids):
            distance = euclidean_distance(point, centroid)
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_centroid_index = i
        clusters[nearest_centroid_index].append(point)
    return clusters

def calculate_new_centroids(clusters):
    new_centroids = []
    for cluster in clusters:
        if not cluster:
            continue
        centroid = tuple(sum(dim)/len(dim) for dim in zip(*cluster))
        new_centroids.append(centroid)
    return new_centroids

def kmeans(data, k, max_iterations=100):
    initial_indices = random.sample(range(len(data)), k)
    centroids = [data[idx] for idx in initial_indices]
    for _ in range(max_iterations):
        clusters = assign_points_to_clusters(centroids, data)
        new_centroids = calculate_new_centroids(clusters)
        if new_centroids == centroids:
            break
        centroids = new_centroids
    return clusters, centroids


data = [
    (1, 2), (1, 4), (1, 0),
    (10, 2), (10, 4), (10, 0),
    (5, 2), (5, 4), (5, 0)
]
k = 3
clusters, centroids = kmeans(data, k)
print("Clusters:", clusters)
print("Centroids:", centroids)