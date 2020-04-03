import json
import operator

import community
import networkx as nx

G_embed = nx.read_graphml("data/graphmls/embedding.graphml")
with open("data/vocabularies/skip_vocab.txt", "r") as f:
    vocabulary = f.read().split("\n")

print(len(G_embed.nodes))
tobedeleted = []
for node in G_embed.nodes:
    if node not in vocabulary:
        tobedeleted.append(node)
for node in tobedeleted:
    G_embed.remove_node(node)
print(len(G_embed.nodes))

pr = nx.pagerank(G_embed)
sorted_pr = sorted(pr.items(), key=operator.itemgetter(1), reverse=True)
sorted_pr = [e[0] for e in sorted_pr]

sorted_pr = sorted_pr[:2773]
tobedeleted2 = [e for e in list(G_embed.nodes) if e not in sorted_pr]
for node in tobedeleted2:
    G_embed.remove_node(node)
print(len(G_embed.nodes))

# giant = max(nx.connected_components(G_embed), key=len)
# tobedeleted3 = [e for e in G_embed.nodes if e not in giant]
# for node in tobedeleted3:
#     G_embed.remove_node(node)
# print(len(G_embed.nodes))

partition = community.best_partition(G_embed)

G_test = nx.Graph()
graph = {}
nodes = []
for node in G_embed.nodes:
    t = {}
    t["id"] = node
    group = str(partition[node])
    t["group"] = group
    nodes.append(t)
    G_test.add_node(node, community=group)

edges = []
for edge in G_embed.edges:
    t = {}
    t["source"] = edge[0]
    t["target"] = edge[1]
    t["value"] = 1
    edges.append(t)
    G_test.add_edge(edge[0], edge[1])

graph["nodes"] = nodes
graph["links"] = edges

with open("data/json/embed_graph.json", "w") as f:
    json.dump(graph, f)

nx.write_graphml(G_test, "data/graphmls/todie.graphml")
