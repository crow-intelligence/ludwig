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
pf = nx.shortest_path(G=G_skip, source="nemzet", target="okos")
pn = nx.shortest_path(G=G_skip, source="nő", target="okos")
print(pf, pn)

pf = nx.shortest_path(G=G_embed, source="nemzet", target="okos")
pn = nx.shortest_path(G=G_embed, source="nő", target="okos")
print(pf, pn)

sp_ffi = nx.shortest_simple_paths(G=G_embed, source="férfi", target="okos")
sp_no = nx.shortest_simple_paths(G=G_embed, source="nő", target="okos")

# chain decomposition
ff_chain = nx.chain_decomposition(G=G_embed, root="férfi")
ff_chain = [e for e in ff_chain if 40 > len(e) > 10]
fn = max([len(e) for e in ff_chain])
fi = [len(e) for e in ff_chain].index(fn)

no_chain = nx.chain_decomposition(G=G_embed, root="nő")
no_chain = [e for e in no_chain if 40 > len(e) > 10]
nn = max([len(e) for e in no_chain])
no = [len(e) for e in no_chain].index(nn)

ff_path = ff_chain[fi]
no_path = no_chain[no]

G = nx.Graph()
for e in ff_path:
    G.add_edge(e[0], e[1])

for e in no_path:
    G.add_edge(e[0], e[1])

nx.write_graphml(G, "data/graphmls/metro1.graphml")