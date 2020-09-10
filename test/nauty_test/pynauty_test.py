import re

# import matplotlib.pyplot as plt
# import networkx as nx
import pynauty as nu

data = []
f = open("set.txt", "r")
data = f.readlines()
f.close()

for i in range(len(data)):
    data[i] = data[i].strip('Set')

li = []
for j in range(len(data)):
    G = nu.Graph(11)
    set = [int(s) for s in re.findall(r'\b\d+\b', data[j])]
    for x in range(0, len(set) - 1, 2):
        G.connect_vertex(set[x]-1, set[x+1]-1)
    print(G.number_of_vertices)
    print(G)
    print("=-"*20)
    li.append(G)

print(nu.isomorphic(li[0], li[1]))


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
