""" import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.cluster as cluster
from sklearn.datasets import make_blobs
import pandas as pd
import time
import hdbscan

blobs, labels = make_blobs(n_samples=2000, n_features=10)
pd.DataFrame(blobs).head()

clusterer = hdbscan.HDBSCAN()

clusterer.fit(blobs)

#HDBSCAN(algorithm='best', alpha=1.0, approx_min_span_tree=True,
#    gen_min_span_tree=False, leaf_size=40, memory=Memory(cachedir=None),
#    metric='euclidean', min_cluster_size=5, min_samples=None, p=None)

clusterer.labels_   #array([2, 2, 2, ..., 2, 2, 0])
print(clusterer.labels_.max())
print(clusterer.probabilities_)

clusterer = hdbscan.HDBSCAN(metric='manhattan')
clusterer.fit(blobs)
print(clusterer.labels_) """

from sklearn.cluster import KMeans
import numpy as np

X = np.array([[1, 2], [1, 4], [1, 0],[10, 2], [10, 4], [10, 0], [4,5],[5,4]])
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
print(kmeans.labels_)
print(kmeans.predict([[0, 0], [12, 3]]))
print(kmeans.cluster_centers_)