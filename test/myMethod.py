import re

import matplotlib.pyplot as plt
import networkx as nx

data = []
f = open("txt/N7.txt", "r")
data = f.readlines()
f.close()

for i in range(len(data)):
    data[i] = data[i].strip('Set')

# for i in range(1, 33):
#     G.add_node(i)


for j in range(len(data)):
    G = nx.Graph()
    set = [int(s) for s in re.findall(r'\b\d+\b', data[j])]
    for x in range(0, len(set) - 1, 2):
        G.add_edge(set[x], set[x + 1], edge_num=1)
    print(G.edges.__len__())
    nx.draw(G, with_labels=True)
    plt.show()

# print(data)
# for i in data:
#     print(i)
#
# set = [int(s) for s in re.findall(r'\b\d+\b', data[j])]
#
# for x in range(0,len(set)-1, 2):
#     G.add_edge(set[x], set[x+1], edge_num=1)


# 连接图
# for j in range(len(data)):
#     G = nx.Graph()
