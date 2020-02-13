import pickle

import numpy as np

with open("data/langmods/seedonly.p", "rb") as f:
    vocab = pickle.load(f)

with open("data/vocabularies/skip_vocab.txt", "r") as f:
    final_vocab = f.read().split("\n")

tobedeleted = [wd for wd in vocab if wd not in final_vocab]
m = np.load("data/langmods/seedonly.npy")
for wd in tobedeleted:
    i = vocab.index(wd)
    m = np.delete(m, i, 0)
    vocab.remove(wd)
print(m.shape)

with open("data/clustering/vocab_clusters.tsv", "r") as f:
    wd_cluster = {}
    for l in f:
        wd, cluster = l.strip().split()
        wd_cluster[wd] = cluster

from sklearn.manifold import TSNE
X_embedded = TSNE(n_components=3)
X_embedded.fit(m)

with open("data/clustering/tsne.tsv", "w") as f:
    h = "Word\tCluster\tX\tY\tZ\n"
    f.write(h)
    for wd in vocab:
        wd = wd.strip()
        wd = wd.replace("\t", "")
        cluster = wd_cluster[wd]
        i = vocab.index(wd)
        x, y, z = X_embedded.embedding_[i]
        x = str(x)
        y = str(y)
        z = str(z)
        o = wd + "\t" + cluster + "\t" + x + "\t" + y + "\t" + z + "\n"
        f.write(o)