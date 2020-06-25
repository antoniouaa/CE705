import numpy as np
from sklearn.cluster import KMeans


class autorefresh_list(dict):
    """
    a dict to collect all the wines associated with
    a cluster
    """
    def __missing__(self, key):
        value = self[key] = []
        return value
    
    def __add__(self, x):
        if not self and isinstance(x, float):
            return x
        raise ValueError
        
    def __sub__(self, x):
        if not self and isinstance(x, float):
            return -1 * x
        raise ValueError

def get_matrix():
    """
    grabs the data from the file and puts them in 
    numpy arrays
    """
    from assignment import load_from_csv
    M = load_from_csv("Data.csv")
    values_array = np.array([x for x in M])
    labels_array = [f"wine{i}" for i in range(values_array.shape[0])]
    return values_array, labels_array

def find_wine_clusters(labels_array, cluster_labels):
    """
    picks out wines which are associated with a cluster and puts them in the autorefresh list
    """
    cluster_to_words = autorefresh_list()
    for i, wine in enumerate(cluster_labels):
        cluster_to_words[wine].append(labels_array[i])
    return cluster_to_words

from timeit import default_timer

start = default_timer()

M, labels_array = get_matrix()
for n_clusters in range(2, 7):
    #Use a k-means model with random initial cluster centroids from the data
    kmeans_model = KMeans(init="random",
        n_clusters=n_clusters, 
        n_init=10)
    kmeans_model.fit(M)
    
    cluster_labels = kmeans_model.labels_
    cluster_inertia = kmeans_model.inertia_
    cluster_to_words = find_wine_clusters(labels_array, cluster_labels)

    print(f"Number of clusters: {n_clusters}")
    for wine in sorted(cluster_to_words):
        print(f"Cluster {wine+1} has {len(cluster_to_words[wine])} entities")
    print()

end = default_timer()
print(f"Time taken: {end-start}")
