import pickle

import numpy as np
from sklearn.neighbors import NearestNeighbors

with open("data/langmods/seedonly.p", "rb") as f:
    vocab = pickle.load(f)

m = np.load("data/langmods/seedonly.npy")
nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)
