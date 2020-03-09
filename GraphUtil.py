import math
import matplotlib.pyplot as plt
import datetime
import networkx as nx
import os


def count_time(info=""):
    """
    统计时间 装饰器
    :param info:
    :return:
    """
    def c_time(func):
        def int_time(*args, **kwargs):
            start_time = datetime.datetime.now()  # 程序开始时间
            func(*args, **kwargs)
            over_time = datetime.datetime.now()  # 程序结束时间
            print('%smake this graph use: %ss' % (info, (over_time - start_time).total_seconds()))
        return int_time
    return c_time


def find_fixed_len_points_one(graph, point, length):
    """
    从一点开始找到某一固定长度路径的其他点(一对)
    :param graph:
    :param point:
    :param length:
    :return:
    """
    point1 = -1
    for nn in graph.G.nodes():
        if point != nn:
            paths = nx.all_shortest_paths(graph.G, point, nn)
            for path in paths:
                if len(path) == length:
                    point1 = nn
                    break
    return point1


def find_len_points(graph, point, length):
    """
    从一点开始找到某一固定长度路径的其他点
    :param graph:
    :param point:
    :param length:
    :return:
    """
    li = []
    result = []
    # 从新增的开始 新增的k5会更远
    for t in graph.G.nodes():
        li.append(t)
    for target in li[::-1]:
        if nx.shortest_path_length(graph.G, point, target) == length - 1:
            result.append(target)

    return result


def find_all_p7_points(graph):
    for source in graph.useful_point:
        for target in graph.G.nodes():
            if nx.shortest_path_length(graph.G, source, target) >= 7 - 1:
                graph.useful_point.remove(source)
                return source, target
    return -1


def add_xpoint(pos1, pos2, f=True):
    """
    计算添加的虚点位置坐标
    :param pos1:
    :param pos2:
    :param f:
    :return:
    """
    # TODO 添加另外两个点
    if (pos2[1] - pos1[1]) != 0:
        mid_point = ((pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2)
        temp = (math.tan(math.pi / 18) ** 2) * ((pos1[0] - mid_point[0]) ** 2 + (pos1[1] - mid_point[1]) ** 2) / (
                1 + ((pos2[0] - pos1[0]) / (pos2[1] - pos1[1])) ** 2)

        x1 = math.sqrt(temp) + mid_point[0]
        y1 = (pos1[0] - pos2[0]) / (pos2[1] - pos1[1]) * (x1 - mid_point[0]) + mid_point[1]

        x2 = -math.sqrt(temp) + mid_point[0]
        y2 = (pos1[0] - pos2[0]) / (pos2[1] - pos1[1]) * (x2 - mid_point[0]) + mid_point[1]
        # f

        # if x1 ** 2 + y1 ** 2 <= x2 ** 2 + y2 ** 2:
        #     return x1, y1
        # else:
        #     return x2, y2
        if f:
            if x1 ** 2 + y1 ** 2 <= x2 ** 2 + y2 ** 2:
                return x1, y1
            else:
                return x2, y2
        else:
            if x1 ** 2 + y1 ** 2 <= x2 ** 2 + y2 ** 2:
                return x2, y2
            else:
                return x1, y1

    else:
        x = (pos1[0] + pos2[0]) / 2
        temp = math.tan(math.pi / 18) * (pos2[0] - pos1[0]) / 2
        y = (pos1[1] + pos2[1]) / 2 + temp
        return x, y


def add_k5(graph, node, f=True):
    """
    添加一个K5
    :param graph:
    :param node:
    :param f:
    :return:
    """
    node1, node2 = node
    pos1 = graph.G.nodes[node1]['position']
    pos2 = graph.G.nodes[node2]['position']
    x, y = add_xpoint(pos1, pos2, f)

    graph.G.add_node(graph.point_index, point_num=0, position=(x, y))
    graph.useful_point.append(graph.point_index)

    graph.G.add_edge(graph.point_index, node1, edge_num=1)
    graph.G.add_edge(graph.point_index, node2, edge_num=1)

    graph.remain_points -= 3
    graph.edge += 9
    graph.point_index += 1


    return graph


def add_k5_(graph, node, f=True):
    """
    添加一个K5
    :param graph:
    :param node:
    :param f:
    :return:
    """
    point3 = graph.point_index
    point2 = graph.point_index + 1
    point1 = graph.point_index + 2



    node1, node2 = node
    pos1 = graph.G.nodes[node1]['position']
    pos2 = graph.G.nodes[node2]['position']
    x, y = add_xpoint(pos1, pos2, f)

    graph.G.add_node(graph.point_index, point_num=0, position=(x, y))
    graph.useful_point.append(graph.point_index)

    graph.G.add_edge(graph.point_index, node1, edge_num=1)
    graph.G.add_edge(graph.point_index, node2, edge_num=1)


    edge = [node1, point3, node2]
    pos1 = graph.G.nodes[edge[0]]['position']
    pos2 = graph.G.nodes[edge[1]]['position']
    pos3 = graph.G.nodes[edge[2]]['position']
    x1, y1 = add_xpoint(pos1, pos2)
    x2, y2 = add_xpoint(pos3, pos2)

    graph.G.add_node(point1, point_num=0, position=(x1, y1))
    graph.G.add_node(point2, point_num=0, position=(x2, y2))
    graph.G.add_edge(point1, edge[0])
    graph.G.add_edge(point1, edge[1])
    graph.G.add_edge(point1, edge[2])
    graph.G.add_edge(point2, edge[0])
    graph.G.add_edge(point2, edge[1])
    graph.G.add_edge(point2, edge[2])
    graph.G.add_edge(point2, point1)

    graph.remain_points -= 3
    graph.edge += 9
    graph.point_index += 3


    return graph


def add_12(graph, edge):
    point = graph.point_index
    pos1 = graph.G.nodes[edge[0]]['position']
    pos2 = graph.G.nodes[edge[1]]['position']
    x, y = add_xpoint(pos1, pos2, f=False)
    graph.G.add_node(point, point_num=0, position=(x, y))
    graph.edge += 2

    graph.G.add_edge(point, edge[0])
    graph.G.add_edge(point, edge[1])
    graph.remain_points -= 1
    graph.point_index += 1
    return True


def add_13(graph, edge):
    point = graph.point_index
    pos1 = graph.G.nodes[edge[0]]['position']
    pos2 = graph.G.nodes[edge[2]]['position']
    x1, y1 = add_xpoint(pos1, pos2, f=False)
    graph.edge += 3
    graph.G.add_node(point, point_num=0, position=(x1, y1))
    graph.G.add_edge(point, edge[0])
    graph.G.add_edge(point, edge[1])
    graph.G.add_edge(point, edge[2])
    graph.remain_points -= 1
    graph.point_index += 1
    return True


def add_25(graph, edge):
    point1 = graph.point_index
    point2 = graph.point_index + 1

    pos1 = graph.G.nodes[edge[0]]['position']
    pos2 = graph.G.nodes[edge[1]]['position']
    x1, y1 = add_xpoint(pos1, pos2)
    x2, y2 = add_xpoint(pos1, pos2, f=False)

    graph.G.add_node(point1, point_num=0, position=(x1, y1))
    graph.G.add_node(point2, point_num=0, position=(x2, y2))
    graph.point_index += 2
    graph.edge += 5
    graph.remain_points -= 2

    graph.G.add_edge(point1, edge[0])
    graph.G.add_edge(point1, edge[1])
    graph.G.add_edge(point2, edge[0])
    graph.G.add_edge(point2, edge[1])
    graph.G.add_edge(point1, point2)


def add_k5e(graph, edge):
    point1 = graph.point_index
    point2 = graph.point_index + 1

    pos1 = graph.G.nodes[edge[0]]['position']
    pos2 = graph.G.nodes[edge[1]]['position']
    pos3 = graph.G.nodes[edge[2]]['position']
    x1, y1 = add_xpoint(pos1, pos2)
    x2, y2 = add_xpoint(pos3, pos2)

    graph.G.add_node(point1, point_num=0, position=(x1, y1))
    graph.G.add_node(point2, point_num=0, position=(x2, y2))
    graph.G.add_edge(point1, edge[0])
    graph.G.add_edge(point1, edge[1])
    graph.G.add_edge(point1, edge[2])
    graph.G.add_edge(point2, edge[0])
    graph.G.add_edge(point2, edge[1])
    graph.G.add_edge(point2, edge[2])
    graph.G.add_edge(point2, point1)
    graph.edge += 7
    graph.remain_points -= 2
    graph.point_index += 2


def mkdir(path="img"):
    if not os.path.exists(path):
        os.makedirs(path)


def save_graph(point, graph, path="img"):
    print("saving img%d.jpg" % point)
    print("Point: %d, Edge: %d" % (point, graph.edge))
    pos = nx.get_node_attributes(graph.G, 'position')
    # pos = nx.circular_layout(graph.G)
    # pos = nx.spectral_layout(graph.G)  # Position nodes using Kamada-Kawai path-length cost-function.
    nx.draw_networkx_nodes(graph.G, pos,
                           nodelist=graph.G.nodes(),
                           node_size=10,

                           node_color='y')

    nx.draw(graph.G, with_labels=False, pos=pos, node_size=10)
    nx.draw_networkx_nodes(graph.G, pos,
                           nodelist=graph.useful_point,
                           node_size=10,
                           node_color='r')
    nx.draw_networkx_nodes(graph.G, pos,
                           nodelist=graph.k5e_point,
                           node_size=10,
                           node_color='y')
    import uuid
    plt.savefig('./%s/%d_%d_%s.png' % (path, point, graph.edge, uuid.uuid1()))
    plt.close()


def show_graph(graph):
    pos = nx.get_node_attributes(graph.G, 'position')
    # pos = nx.circular_layout(graph.G)
    # pos = nx.spectral_layout(graph.G)  # Position nodes using Kamada-Kawai path-length cost-function.
    nx.draw_networkx_nodes(graph.G, pos,
                           nodelist=graph.G.nodes(),
                           node_color='y')

    nx.draw_networkx_nodes(graph.G, pos,
                           nodelist=graph.useful_point,
                           node_color='r')
    nx.draw(graph.G, with_labels=True, pos=pos)
    nx.draw_networkx_nodes(graph.G, pos,
                           nodelist=graph.useful_point,
                           node_color='r')
    plt.show()


# 判断图中是否出现C6
def is_more_6(data, source=None):
    if source is None:
        nodes = data.G.nodes()
    else:
        nodes = source
    cycle_stack = []
    output_cycles = set()

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

        stack = [(start, iter(data.G[start]))]
        while stack:
            parent, children = stack[-1]
            try:
                child = next(children)

                if child not in cycle_stack:
                    cycle_stack.append(child)
                    stack.append((child, iter(data.G[child])))
                else:
                    i = cycle_stack.index(child)
                    if i < len(cycle_stack) - 2:
                        if len(get_hashable_cycle(cycle_stack[i:])) == 6:
                        # if len(get_hashable_cycle(cycle_stack[i:])) <= 6 and len(
                        #         get_hashable_cycle(cycle_stack[i:])) != 3:
                            return False

            except StopIteration:
                stack.pop()
                cycle_stack.pop()

    return True

#
# def edge_point_one(graph, edge):
#     point = graph.point_index
#     if len(edge) == 0:
#         return False
#     elif len(edge) == 2:
#         pos1 = graph.G.nodes[edge[0]]['position']
#         pos2 = graph.G.nodes[edge[1]]['position']
#         x, y = add_xpoint(pos1, pos2, f=False)
#         graph.G.add_node(point, point_num=0, position=(x, y))
#         graph.edge += 2
#
#         graph.G.add_edge(point, edge[0])
#         graph.G.add_edge(point, edge[1])
#     elif len(edge) == 3:
#         pos1 = graph.G.nodes[edge[0]]['position']
#         pos2 = graph.G.nodes[edge[2]]['position']
#         x1, y1 = add_xpoint(pos1, pos2, f=False)
#         graph.edge += 3
#         graph.G.add_node(point, point_num=0, position=(x1, y1))
#         graph.G.add_edge(point, edge[0])
#         graph.G.add_edge(point, edge[1])
#         graph.G.add_edge(point, edge[2])
#
#     graph.remain_points -= 1
#     graph.point_index += 1
#     return True
#
#
# def edge_point_two(graph, edge):
#     edge_point_one(graph, edge)
#     flag = edge_point_one(graph, edge)
#     if flag:
#         point1 = graph.point_index - 1
#         point2 = point1 - 1
#         graph.edge += 1
#         # 两点最后相连
#         graph.G.add_edge(point1, point2)
