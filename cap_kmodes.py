import numpy as np
from kmodes import kprototypes

kp = kprototypes.KPrototypes(n_clusters=7, init='Cao', verbose=2)

X= df_small.values
clusters = kp.fit_predict(X, categorical=[1, 2,3,7,8])

print "Cluster centroids"
print(kp.cluster_centroids_)

print "Training stats"
print(kproto.cost_)
print(kproto.n_iter_)

#getting cost 
cost = []
for i in range(1,11):
    kp= kprototypes.KPrototypes(n_clusters=i, init='Cao', verbose=2)
    clusters = kp.fit_predict(X, categorical=[0,1, 2,3,4,5,6,8,9])
    cost.append(kp.cost_)
