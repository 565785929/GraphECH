import hashlib
import re
import pynauty as nu
from pynauty import certificate
import networkx as nx


def make_graph():
    G = nx.Graph()
    G.add_node(1, point_num=2, position=(0, 2))
    G.add_node(2, point_num=2, position=(1.5, 1.5))
    G.add_node(3, point_num=2, position=(2, 0))
    G.add_node(4, point_num=2, position=(1.5, -1.5))
    G.add_node(5, point_num=2, position=(0, -2))
    G.add_node(6, point_num=2, position=(-1.5, -1.5))
    G.add_node(7, point_num=2, position=(-2, 0))
    G.add_node(8, point_num=2, position=(-1.5, 1.5))

    for _ in range(1, 9):
        G.add_edge(_, _ % 8 + 1, edge_num=1)
    return G

def make_graph2():
    G = nx.Graph()
    G.add_node(1, point_num=2, position=(1, 2))
    G.add_node(2, point_num=2, position=(1, 1.5))
    G.add_node(3, point_num=2, position=(1, 0))
    G.add_node(4, point_num=2, position=(1, -1.5))
    G.add_node(5, point_num=2, position=(1, -2))
    G.add_node(6, point_num=2, position=(-1, -1.5))
    G.add_node(7, point_num=2, position=(-2, 0))
    G.add_node(8, point_num=2, position=(-1, 1.5))

    G.add_edge(1, 6, edge_num=1)
    G.add_edge(1, 5, edge_num=1)
    G.add_edge(2, 7, edge_num=1)
    G.add_edge(2, 8, edge_num=1)
    G.add_edge(5, 8, edge_num=1)
    G.add_edge(3, 4, edge_num=1)
    G.add_edge(3, 6, edge_num=1)
    G.add_edge(4, 7, edge_num=1)
    return G

if __name__ == '__main__':
    a = make_graph()
    b = make_graph2()

    aa = nu.Graph(a.size())

    for x in a.edges:
        aa.connect_vertex(x[0]-1, x[1]-1)
    print(aa)


    bb = nu.Graph(b.size())

    for x in b.edges:
        bb.connect_vertex(x[0]-1, x[1]-1)
    print(bb)

    print(nu.isomorphic(aa, bb))

    aaa = certificate(aa)
    bbb = certificate(bb)

    aaaa = hashlib.sha256(aaa)
    bbbb = hashlib.sha256(bbb)
    a1 = (aaaa.hexdigest())
    b1 = (bbbb.hexdigest())


    test = set()
    test.add(a1)
    if b1 in test:
        print("!")


def get_graph_ceritficate(g):
    temp = nu.Graph(g.size())
    for _ in g.edges:
        temp.connect_vertex(_[0] - 1, _[1] - 1)
    return hashlib.sha256(certificate(temp)).hexdigest()

