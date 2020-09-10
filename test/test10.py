import re
import networkx as nx
import matplotlib.pyplot as plt

def is_con_edges(G, source=None):
    if source is None:
        nodes = G.nodes()
    else:
        nodes = source
    cycle_stack = []

    def get_hashable_cycle(cycle):
        m = min(cycle)
        mi = cycle.index(m)
        mi_plus_1 = mi + 1 if mi < len(cycle) - 1 else 0
        if cycle[mi - 1] > cycle[mi_plus_1]:
            result = cycle[mi:] + cycle[:mi]
        else:
            result = list(reversed(cycle[:mi_plus_1])) + list(reversed(cycle[mi_plus_1:]))
        return tuple(result)

    for start in nodes:
        if start in cycle_stack:
            continue
        cycle_stack.append(start)

        stack = [(start, iter(G[start]))]
        while stack:
            parent, children = stack[-1]
            try:
                child = next(children)

                if child not in cycle_stack:
                    cycle_stack.append(child)
                    stack.append((child, iter(G[child])))
                else:
                    i = cycle_stack.index(child)
                    if i < len(cycle_stack) - 2:
                        if len(get_hashable_cycle(cycle_stack[i:])) == 6:
                            return False

            except StopIteration:
                stack.pop()
                cycle_stack.pop()
    return True

data = []
f=open("txt/N7.txt","r")
data= f.readlines()
f.close()

for i in range(len(data)):
    data[i]=data[i].strip('Set')
# 连接图
for j in range(len(data)):
    G = nx.Graph()
    G.add_node(1, point_num=2, position=(0, 1))
    G.add_node(2, point_num=2, position=(-2, 0))
    G.add_node(3, point_num=2, position=(-1.5, -2))
    G.add_node(4, point_num=2, position=(1.5, -2))
    G.add_node(5, point_num=2, position=(2, 0))
    G.add_node(6, point_num=2, position=(1.5, 0.7))
    G.add_node(7, point_num=2, position=(1, 1.5))

    set = [int(s) for s in re.findall(r'\b\d+\b', data[j])]
    for x in range(0,len(set)-1,2):
        G.add_edge(set[x],set[x+1], edge_num=1)
    print(is_con_edges(G))
    print(nx.cycle_basis(G))
    print(nx.find_cycle(G, 1))
    # print(nx.simple_cycles(G))
    print(nx.minimum_cycle_basis(G))
    set.clear()
    # pos = nx.get_node_attributes(G, 'position')
    nx.draw(G, with_labels=True )
    plt.savefig('image/N7/%d_%d_%s.png' % (j,len(G.edges),is_con_edges(G)))
    G.clear()
    plt.close()
    plt.show()
