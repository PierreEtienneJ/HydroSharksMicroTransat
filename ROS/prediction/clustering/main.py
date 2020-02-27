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
import hdbscan
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import time
t0=time.time()
#X = 1*np.random.random((100,2))-1
X=[[i/1000, math.exp(i/1000)] for i in range(1000)]
X+=[[i/1000, math.exp(i/1000)+0.5] for i in range(1000)]
for i in range(len(X)):
    X[i][0]+=random.random()*0.2
X+=[[random.random(), 3*random.random()] for i in range(100)]    
kmeans = KMeans(n_clusters=9, random_state=0).fit(X)
hdb=hdbscan.HDBSCAN(metric='manhattan').fit(X)
A=hdb.labels_   #a mon avis si -1 : hors de génération sinon c'est un groupement
print(A)
ncluster=max(A)+1
print(ncluster)
color=["b", "g", "r", "c", "m",  "y", "k"]
form=[".", "<",">"]

D=[]
for i in range(max(A)+2):
    D.append([])

for i in range(len(A)):
    D[A[i]].append([X[i][0], X[i][1]])

for i in range(len(D)):
    plt.plot([D[i][j][0] for j in range(len(D[i]))] , [D[i][j][1] for j in range(len(D[i]))], form[i%len(form)]+color[i%len(color)])

        
    #print(D[i][:][:])

plt.show()
print([len(D[i]) for i in range(len(D))])

print(time.time()-t0)
    
#print(kmeans.labels_)
#print(kmeans.predict([[0, 0], [8, 3]]))
C=kmeans.cluster_centers_

#plt.plot(X[:,0], X[:,1], "*r")
#plt.plot(C[:,0], C[:,1], "^g")
#plt.show()