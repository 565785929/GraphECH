from final import *

G = None
edge = 0
point_index = 9
sys_dict = {1: 1, 2: 8, 3: 7, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2}

useful_point = []
n = 8
data = Data(G, n, edge, point_index, sys_dict, useful_point)


print(data.G.edges)
if (2, 1) in data.G.edges:
    print("yes")
data.G.add_edge(1, 6, edge_num=1)

data.G.remove_edge(1, 6)
pos = nx.get_node_attributes(data.G, 'position')
nx.draw(data.G, with_labels=True, pos=pos)
plt.show()
plt.close()
print(is_more_6(data))

print(i for i in iter(data.G[1]))

print(data.G[2])