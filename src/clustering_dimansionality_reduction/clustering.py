import pickle

from sklearn.cluster import KMeans
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

kmeans = KMeans(n_clusters=15, random_state=0).fit(m)
labels = list(kmeans.labels_)
print(max(labels))

with open("data/clustering/vocab_clusters.tsv", "w") as outfile:
    for e in zip(vocab, labels):
        if e[1] > -1:
            o = e[0] + "\t" + str(e[1]) + "\n"
            outfile.write(o)
