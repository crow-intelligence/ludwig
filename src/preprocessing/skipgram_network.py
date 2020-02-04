import operator
from os import listdir
from os.path import isfile, join

import math
import networkx as nx
from bounter import bounter
from nltk import skipgrams


in_path = "data/stemmed_text"
txts = [f for f in listdir(in_path) if isfile(join(in_path, f))]

with open("data/external/stopwords.txt", "r") as f:
    stopwords = set(f.read().strip().split("\n"))

counts = bounter(size_mb=1024)
word_freqs = {}
for txt in txts:
    with open(join(in_path, txt), "r") as f:
        text = f.read().split()
    text = [wd for wd in text if wd not in stopwords]
    for wd in text:
        if wd in word_freqs:
            word_freqs[wd] += 1
        else:
            word_freqs[wd] = 1
    skips = list(skipgrams(text, 2, 5))
    skips = ['@'.join(t) for t in skips]
    counts.update(skips)

sorted_x = sorted(word_freqs.items(), key=operator.itemgetter(1),
                  reverse=True)
limit = math.floor(len(sorted_x) * 0.80)
sorted_x = sorted_x[:limit]
words = [e[0] for e in sorted_x]
G = nx.Graph()
for e in counts.iteritems():
    st = e[0]
    if e[1] > 1:
        try:
            source, target = st.split("@")
            if source in words and target in words:
                G.add_edge(source, target, weight=e[1])
        except Exception as exc:
            continue
nx.write_graphml(G, "data/graphmls/skipgrams.graphml")
