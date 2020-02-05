from os import listdir
from os.path import isfile, join

import networkx as nx
from bounter import bounter
from nltk import skipgrams


in_path = "data/seedonly"
txts = [f for f in listdir(in_path) if isfile(join(in_path, f))]

with open("data/external/stopwords.txt", "r") as f:
    stopwords = set(f.read().strip().split("\n"))

counts = bounter(size_mb=1024)
for txt in txts:
    with open(join(in_path, txt), "r") as f:
        text = f.read().split()
    text = [wd for wd in text if wd not in stopwords]
    skips = list(skipgrams(text, 2, 5))
    skips = ['@'.join(t) for t in skips]
    counts.update(skips)

G = nx.Graph()
i = 0
for skip, freq in counts.iteritems():
    if freq > 50:
        try:
            source, target = skip.split("@")
            G.add_edge(source, target, weight=freq)
            if source not in G:
                G.add_node(source)
            if target not in G:
                G.add_node(target)
            i += 1
        except Exception as exc:
            print(exc)
            continue
nx.write_graphml(G, "data/graphmls/skipgrams.graphml")
