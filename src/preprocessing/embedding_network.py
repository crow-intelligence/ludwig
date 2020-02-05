import operator
import pickle
from collections import Counter

import networkx as nx
import numpy as np
from bounter import bounter

with open("data/langmods/seedonly.p", "rb") as f:
    vocab = pickle.load(f)

m = np.load("data/langmods/seedonly.npy")

G = nx.Graph()
counts = bounter(size_mb=1024)

for i in range(len(vocab)):
    source = vocab[i]
    dists = np.dot(m, m[i])
    closests = sorted(list(dists), reverse=True)[:6]
    edges = []
    for c in closests:
        wordid = list(dists).index(c)
        target = vocab[wordid]
        if source != target:
            t = "@".join(sorted((source, target)))
            edges.append(t)
    counts.update(edges)

G = nx.Graph()
i = 0
for skip, freq in counts.iteritems():
    if freq > 0:
        try:
            source, target = skip.split("@")
            G.add_edge(source, target, weight=freq)
            if source not in G:
                G.add_node(source)
            if target not in G:
                G.add_node(target)
            i += 1
            print(f"we have {i} edges")
        except Exception as exc:
            print(exc)
            continue
nx.write_graphml(G, "data/graphmls/embedding.graphml")

