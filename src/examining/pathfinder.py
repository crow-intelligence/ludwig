import networkx as nx

G_skip = nx.read_graphml("data/graphmls/skipgrams.graphml")
G_embed = nx.read_graphml("data/graphmls/embedding.graphml")

# vocabulary
vocabulary_skip = list(G_skip.nodes)
with open("data/vocabularies/skip_vocab.txt", "w") as f:
    for wd in vocabulary_skip:
        f.write(wd + "\n")
vocabulary_embed = list(G_embed.nodes)
with open("data/vocabularies/embed_vocab.txt", "w") as f:
    for wd in vocabulary_embed:
        f.write(wd + "\n")

# path btw two nodes
pf = nx.shortest_path(G=G_skip, source="férfi", target="okos")
pn = nx.shortest_path(G=G_skip, source="nő", target="okos")
print(pf, pn)

pf = nx.shortest_path(G=G_embed, source="férfi", target="okos")
pn = nx.shortest_path(G=G_embed, source="nő", target="okos")
print(pf, pn)