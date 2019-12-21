import math
import time
import copy
import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue


class Data:
    def __init__(self, G, n, edge, point_index, sys_dict, useful_point):
        if G == None:
            self.G, self.n, self.edge = self.init(n, edge)
        else:
            self.G = G
            self.n = n
            self.edge = edge
        self.point_index = point_index
        self.sys_dict = sys_dict
        self.useful_point = useful_point

    # 初始化母图C8
    def init(self, n, edge):
        G = nx.Graph()

        G.add_node(1, point_num=2, position=(0, 2))
        G.add_node(2, point_num=2, position=(1.5, 1.5))
        G.add_node(3, point_num=2, position=(2, 0))
        G.add_node(4, point_num=2, position=(1.5, -1.5))
        G.add_node(5, point_num=2, position=(0, -2))
        G.add_node(6, point_num=2, position=(-1.5, -1.5))
        G.add_node(7, point_num=2, position=(-2, 0))
        G.add_node(8, point_num=2, position=(-1.5, 1.5))
        n -= 8

        for point in range(1, 9):
            point_x = point % 8 + 1
            G.add_edge(point, point_x, edge_num=1)
        edge += 8

        return G, n, edge


# 添加四对虚点
def add_four_pairs(data):
    for index in range(1, 9):
        if index != 8:
            data = add_k5(data, index, index + 1)
        else:
            data = add_k5(data, index, 1)

    point = data.point_index - 8
    sys_point = data.point_index - 1
    for _ in range(4):
        data.sys_dict[point] = sys_point
        data.sys_dict[sys_point] = point
        point += 1
        sys_point -= 1

    useful18 = []
    useful27 = []
    useful36 = []
    useful45 = []
    while len(data.useful_point) > 0:
        p1 = data.useful_point[0]
        p2 = data.useful_point[1]
        p3 = data.useful_point[2]
        p4 = data.useful_point[3]
        p5 = data.useful_point[4]
        p6 = data.useful_point[5]
        p7 = data.useful_point[6]
        p8 = data.useful_point[7]
        useful18.append(p1[0])
        useful18.append(p8[0])
        useful27.append(p2[0])
        useful27.append(p7[0])
        useful36.append(p3[0])
        useful36.append(p6[0])
        useful45.append(p4[0])
        useful45.append(p5[0])
        data.useful_point.clear()
    data.useful_point.append(useful18)
    data.useful_point.append(useful27)
    data.useful_point.append(useful36)
    data.useful_point.append(useful45)

    return data


# 计算添加的虚点位置坐标
def add_xpoint(pos1, pos2):
    if (pos2[1] - pos1[1]) != 0:
        mid_point = ((pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2)
        temp = (math.tan(math.pi / 18) ** 2) * ((pos1[0] - mid_point[0]) ** 2 + (pos1[1] - mid_point[1]) ** 2) / (
            1 + ((pos2[0] - pos1[0]) / (pos2[1] - pos1[1])) ** 2)

        x1 = math.sqrt(temp) + mid_point[0]
        y1 = (pos1[0] - pos2[0]) / (pos2[1] - pos1[1]) * (x1 - mid_point[0]) + mid_point[1]

        x2 = -math.sqrt(temp) + mid_point[0]
        y2 = (pos1[0] - pos2[0]) / (pos2[1] - pos1[1]) * (x2 - mid_point[0]) + mid_point[1]

        if x1 ** 2 + y1 ** 2 <= x2 ** 2 + y2 ** 2:
            return x1, y1
        else:
            return x2, y2
    else:
        x = (pos1[0] + pos2[0]) / 2
        temp = math.tan(math.pi / 18) * (pos2[0] - pos1[0]) / 2
        y = (pos1[1] + pos2[1]) / 2 + temp
        return x, y


# 添加一个K5
def add_k5(data, node1, node2):
    pos1 = data.G.nodes[node1]['position']
    pos2 = data.G.nodes[node2]['position']
    x, y = add_xpoint(pos1, pos2)

    data.G.add_node(data.point_index, point_num=0, position=(x, y))
    data.useful_point.append([data.point_index])

    data.G.add_edge(data.point_index, node1, edge_num=1)
    data.G.add_edge(data.point_index, node2, edge_num=1)

    data.n = data.n - 3
    data.edge = data.edge + 9
    data.point_index += 1

    return data


# 一对对称点之间找P6或P5
def connect_sys_points(data, point, sys_point):
    paths = nx.all_shortest_paths(data.G, point, sys_point)
    is_deal = False
    data1 = copy.deepcopy(data)
    data2 = copy.deepcopy(data)
    for path in paths:
        if len(path) == 6:
            data1 = add_one_point_k5e(data1, point, sys_point)
            data2 = add_one_point_2k5(data2, print, sys_point)
            if data.n != data1.n:
                is_deal = True
            elif data.n != data2.n:
                is_deal = True
            else:
                print('一对对称点之间未找到P6')
        elif len(path) == 5:
            data1 = add_two_points_3k5(data1, point, sys_point)
            data2 = add_two_points_2k5(data2, point, sys_point)
            if data.n != data1.n:
                is_deal = True
            elif data.n != data2.n:
                is_deal = True
            else:
                print('一对对称点之间未找到P5')
        else:
            continue

    return is_deal, data, data1, data2


# 一对对称点与其他点之间，长度为P6(四对)
def connect_no_sys_point_p6_four(data, point, sys_point):
    is_deal = False
    point_nodes = find_fixed_len_points_four(data, point, 6)
    sys_point_nodes = find_fixed_len_points_four(data, sys_point, 6)
    data1 = copy.deepcopy(data)
    data2 = copy.deepcopy(data)
    if len(point_nodes) > 0 and len(sys_point_nodes) > 0:
        if data.n >= 6 and data.n < 14:
            for point_node in point_nodes:
                temp_data2 = add_one_point_k5e(data2, point, point_node)
                if temp_data2.n != data2.n:
                    data2 = temp_data2
                    break
            for sys_point_node in sys_point_nodes:
                temp_data2 = add_one_point_k5e(data2, sys_point, sys_point_node)
                if temp_data2.n != data2.n:
                    data2 = temp_data2
                    break
            if data.n != data2.n:
                # data2.sys_dict[data2.point_index - 2] = data2.point_index - 1
                # data2.sys_dict[data2.point_index - 1] = data2.point_index - 2
                is_deal = True

        if data.n >= 14:
            for point_node in point_nodes:
                temp_data1 = add_one_point_2k5(data1, point, point_node)
                if temp_data1.n != data1.n:
                    data1 = temp_data1
                    break
            for sys_point_node in sys_point_nodes:
                temp_data1 = add_one_point_2k5(data1, sys_point, sys_point_node)
                if temp_data1.n != data1.n:
                    data1 = temp_data1
                    break
            # if (data.n - data1.n) == 14:
            #     data1.sys_dict[data1.point_index - 6] = data1.point_index - 3
            #     data1.sys_dict[data1.point_index - 3] = data1.point_index - 6
            #     data1.sys_dict[data1.point_index - 5] = data1.point_index - 2
            #     data1.sys_dict[data1.point_index - 2] = data1.point_index - 5
            #     data1.sys_dict[data1.point_index - 4] = data1.point_index - 1
            #     data1.sys_dict[data1.point_index - 1] = data1.point_index - 4
            for point_node in point_nodes:
                temp_data2 = add_one_point_k5e(data2, point, point_node)
                if temp_data2.n != data2.n:
                    data2 = temp_data2
                    break
            for sys_point_node in sys_point_nodes:
                temp_data2 = add_one_point_k5e(data2, sys_point, sys_point_node)
                if temp_data2.n != data2.n:
                    data2 = temp_data2
                    break
            # if (data.n - data2.n) == 6:
            #     data2.sys_dict[data2.point_index - 2] = data2.point_index - 1
            #     data2.sys_dict[data2.point_index - 1] = data2.point_index - 2
            if data.n != data1.n:
                is_deal = True
            elif data.n != data2.n:
                is_deal = True
            else:
                print('该对对称点未处理')

    return is_deal, data, data1, data2


# 一对对称点与其他点之间，长度为P5(四对)
def connect_no_sys_point_p5_four(data, point, sys_point):
    is_deal = False
    point_nodes = find_fixed_len_points_four(data, point, 5)
    sys_point_nodes = find_fixed_len_points_four(data, sys_point, 5)
    data1 = copy.deepcopy(data)
    data2 = copy.deepcopy(data)
    if len(point_nodes) > 0 and len(sys_point_nodes) > 0:
        if data.n >= 16 and data.n < 22:
            for point_node in point_nodes:
                temp_data2 = add_two_points_2k5(data2, point, point_node)
                if temp_data2.n != data2.n:
                    data2 = temp_data2
                    break
            for sys_point_node in sys_point_nodes:
                temp_data2 = add_two_points_2k5(data2, sys_point, sys_point_node)
                if temp_data2.n != data2.n:
                    data2 = temp_data2
                    break
            if data.n != data2.n:
                is_deal = True

        if data.n >= 22:
            for point_node in point_nodes:
                temp_data1 = add_two_points_3k5(data1, point, point_node)
                if temp_data1.n != data1.n:
                    data1 = temp_data1
                    break
            for sys_point_node in sys_point_nodes:
                temp_data1 = add_two_points_3k5(data1, sys_point, sys_point_node)
                if temp_data1.n != data1.n:
                    data1 = temp_data1
                    break
            for point_node in point_nodes:
                temp_data2 = add_two_points_2k5(data2, point, point_node)
                if temp_data2.n != data2.n:
                    data2 = temp_data2
                    break
            for sys_point_node in sys_point_nodes:
                temp_data2 = add_two_points_2k5(data2, sys_point, sys_point_node)
                if temp_data2.n != data2.n:
                    data2 = temp_data2
                    break
            if data.n != data1.n:
                is_deal = True
            elif data.n != data2.n:
                is_deal = True
            else:
                print('该对对称点未处理')

    return is_deal, data, data1, data2


# 一个点单独处理(四对)
def connect_no_sys_point_four(data, point):
    points_p6 = find_fixed_len_points_four(data, point, 6)
    is_deal1 = False
    data1 = copy.deepcopy(data)
    data2 = copy.deepcopy(data)
    data3 = copy.deepcopy(data)
    if len(points_p6) > 0:
        for node_pointnum_2 in points_p6:
            if not is_deal1:
                data1 = add_one_point_2k5(data1, point, node_pointnum_2)
                data2 = add_one_point_k5e(data2, point, node_pointnum_2)
                data3 = add_one_point_k2(data3, point, node_pointnum_2)
                if data.n != data1.n:
                    is_deal1 = True
                if data.n != data2.n:
                    is_deal1 = True
                if data.n != data3.n:
                    is_deal1 = True
            else:
                break

    points_p5 = find_fixed_len_points_four(data, point, 5)
    is_deal2 = False
    data4 = copy.deepcopy(data)
    data5 = copy.deepcopy(data)
    if len(points_p5) > 0:
        for node_pointnum_2 in points_p5:
            if not is_deal2:
                data4 = add_two_points_3k5(data4, point, node_pointnum_2)
                data5 = add_two_points_2k5(data5, point, node_pointnum_2)
                if data.n != data4.n:
                    is_deal2 = True
                if data.n != data5.n:
                    is_deal2 = True
            else:
                break

    return data, data1, data2, data3, data4, data5


# P6+1，k5-e
def add_one_point_k5e(data, node1, node2):
    if data.n >= 3:
        pos1 = data.G.nodes[node1]['position']
        pos2 = data.G.nodes[node2]['position']

        x = (pos1[0] + 2 * pos2[0]) / 3
        y = (pos1[1] + 2 * pos2[1]) / 3

        data.G.add_node(data.point_index, point_num=0, position=(x, y))
        data.useful_point.append([data.point_index])
        data.G.add_edge(node1, data.point_index, edge_num=0)
        data.G.add_edge(data.point_index, node2, edge_num=0)

        data.point_index += 1
        data.n = data.n - 1

        if is_more_6(data):
            if data.G.nodes[node2]['point_num'] != 2 and data.G.nodes[node2]['point_num'] != 1:
                data.G.nodes[node2]['point_num'] = 1
                find_useful_point(node2, data.useful_point)
            data.G.nodes[node1]['point_num'] = 1

            data.n = data.n - 2
            data.edge = data.edge + 9
        else:
            data.G.remove_node(data.point_index - 1)
            data.point_index -= 1
            data.n += 1

    return data


# P6+1，2k5
def add_one_point_2k5(data, node1, node2):
    if data.n >= 7:
        pos1 = data.G.nodes[node1]['position']
        pos2 = data.G.nodes[node2]['position']

        x = (pos1[0] + 2 * pos2[0]) / 3
        y = (pos1[1] + 2 * pos2[1]) / 3

        data.G.add_node(data.point_index, point_num=0, position=(x, y))
        data.useful_point.append([data.point_index])
        data.G.add_edge(node1, data.point_index, edge_num=0)
        data.G.add_edge(data.point_index, node2, edge_num=0)

        data.point_index += 1
        data.n = data.n - 1

        if is_more_6(data):
            if data.G.nodes[node2]['point_num'] != 2 and data.G.nodes[node2]['point_num'] != 1:
                data.G.nodes[node2]['point_num'] = 1
                find_useful_point(node2, data.useful_point)
            data.G.nodes[node1]['point_num'] = 1

            data.G.nodes[data.point_index - 1]['point_num'] = 1
            data.useful_point.remove([data.point_index - 1])

            data = add_k5(data, node1, data.point_index - 1)
            data = add_k5(data, data.point_index - 2, node2)

            data.edge = data.edge + 2
        else:
            data.G.remove_node(data.point_index - 1)
            data.point_index -= 1
            data.n += 1

    return data


# P6+1，K2(四对)
def add_one_point_k2(data, node1, node2):
    if data.n > 0:
        pos1 = data.G.nodes[node1]['position']
        pos2 = data.G.nodes[node2]['position']

        x = (pos1[0] + 2 * pos2[0]) / 3
        y = (pos1[1] + 2 * pos2[1]) / 3

        data.G.add_node(data.point_index, point_num=0, position=(x, y))
        data.useful_point.append([data.point_index])
        data.G.add_edge(node1, data.point_index, edge_num=0)
        data.G.add_edge(data.point_index, node2, edge_num=0)

        data.point_index += 1
        data.n = data.n - 1

        if is_more_6(data):
            if data.G.nodes[node2]['point_num'] != 2 and data.G.nodes[node2]['point_num'] != 1:
                data.G.nodes[node2]['point_num'] = 1
                find_useful_point(node2, data.useful_point)
            data.G.nodes[node1]['point_num'] = 1

            data.edge = data.edge + 2
        else:
            data.G.remove_node(data.point_index - 1)
            data.point_index -= 1
            data.n += 1

    return data


# P5+2，3k5
def add_two_points_3k5(data, node1, node2):
    node_dict = {}

    if data.n >= 11:
        pos1 = data.G.nodes[node1]['position']
        pos2 = data.G.nodes[node2]['position']

        node_dict.update({node1: pos1[0]})
        node_dict.update({node2: pos2[0]})

        x1 = (2 * pos1[0] + pos2[0]) / 3
        y1 = (2 * pos1[1] + pos2[1]) / 3

        x2 = (pos1[0] + 2 * pos2[0]) / 3
        y2 = (pos1[1] + 2 * pos2[1]) / 3

        data.G.add_node(data.point_index, point_num=0, position=(x1, y1))
        node_dict.update({data.point_index: x1})
        data.useful_point.append([data.point_index])
        data.point_index += 1

        data.G.add_node(data.point_index, point_num=0, position=(x2, y2))
        node_dict.update({data.point_index: x2})
        data.useful_point.append([data.point_index])
        data.point_index += 1

        data.n = data.n - 2

        sorted_nodes_list = sort_nodes(node_dict)
        for index in range(len(sorted_nodes_list)):
            if index != len(sorted_nodes_list) - 1:
                data.G.add_edge(sorted_nodes_list[index], sorted_nodes_list[index + 1], edge_num=0)

        if is_more_6(data):
            if data.G.nodes[node2]['point_num'] != 2 and data.G.nodes[node2]['point_num'] != 1:
                data.G.nodes[node2]['point_num'] = 1
                find_useful_point(node2, data.useful_point)
            data.G.nodes[node1]['point_num'] = 1

            data.sys_dict[data.point_index - 2] = data.point_index - 1
            data.sys_dict[data.point_index - 1] = data.point_index - 2

            data.G.nodes[data.point_index - 2]['point_num'] = 1
            data.G.nodes[data.point_index - 1]['point_num'] = 1
            data.useful_point.remove([data.point_index - 2])
            data.useful_point.remove([data.point_index - 1])

            for index in range(len(sorted_nodes_list)):
                if index != len(sorted_nodes_list) - 1:
                    data = add_k5(data, sorted_nodes_list[index], sorted_nodes_list[index + 1])
            data.sys_dict[data.point_index - 3] = data.point_index - 1
            data.sys_dict[data.point_index - 2] = data.point_index - 2
            data.sys_dict[data.point_index - 1] = data.point_index - 3

            sys_points = []
            i = 0
            mid = []
            while len(data.useful_point) > 0:
                if i >= 3:
                    break
                p = data.useful_point.pop()
                if i == 0 or i == 2:
                    sys_points.append(p[0])
                else:
                    mid = p
                i += 1
            data.useful_point.append(sys_points)
            data.useful_point.append(mid)

            data.edge = data.edge + 3
        else:
            data.G.remove_node(data.point_index - 1)
            data.G.remove_node(data.point_index - 2)
            data.point_index = data.point_index + 2
            data.n = data.n + 2

    return data


# P5+2，2k5
def add_two_points_2k5(data, node1, node2):
    node_dict = {}

    if data.n >= 8:
        pos1 = data.G.nodes[node1]['position']
        pos2 = data.G.nodes[node2]['position']

        node_dict.update({node1: pos1[0]})
        node_dict.update({node2: pos2[0]})

        x1 = (2 * pos1[0] + pos2[0]) / 3
        y1 = (2 * pos1[1] + pos2[1]) / 3

        x2 = (pos1[0] + 2 * pos2[0]) / 3
        y2 = (pos1[1] + 2 * pos2[1]) / 3

        data.G.add_node(data.point_index, point_num=0, position=(x1, y1))
        node_dict.update({data.point_index: x1})
        data.useful_point.append([data.point_index])
        data.point_index += 1

        data.G.add_node(data.point_index, point_num=0, position=(x2, y2))
        node_dict.update({data.point_index: x2})
        data.useful_point.append([data.point_index])
        data.point_index += 1

        data.n = data.n - 2

        sorted_nodes_list = sort_nodes(node_dict)
        for index in range(len(sorted_nodes_list)):
            if index != len(sorted_nodes_list) - 1:
                data.G.add_edge(sorted_nodes_list[index], sorted_nodes_list[index + 1], edge_num=0)

        if is_more_6(data):
            if data.G.nodes[node2]['point_num'] != 2 and data.G.nodes[node2]['point_num'] != 1:
                data.G.nodes[node2]['point_num'] = 1
                find_useful_point(node2, data.useful_point)
            data.G.nodes[node1]['point_num'] = 1

            data.sys_dict[data.point_index - 2] = data.point_index - 1
            data.sys_dict[data.point_index - 1] = data.point_index - 2

            data.G.nodes[data.point_index - 2]['point_num'] = 1
            data.G.nodes[data.point_index - 1]['point_num'] = 1
            data.useful_point.remove([data.point_index - 2])
            data.useful_point.remove([data.point_index - 1])

            data = add_k5(data, sorted_nodes_list[0], sorted_nodes_list[1])
            data = add_k5(data, sorted_nodes_list[2], sorted_nodes_list[3])

            data.sys_dict[data.point_index - 2] = data.point_index - 1
            data.sys_dict[data.point_index - 1] = data.point_index - 2

            sys_points = []
            i = 0
            while len(data.useful_point) > 0:
                if i >= 2:
                    break
                p = data.useful_point.pop()
                sys_points.append(p[0])
                i += 1
            data.useful_point.append(sys_points)

            data.edge = data.edge + 3
        else:
            data.G.remove_node(data.point_index - 1)
            data.G.remove_node(data.point_index - 2)
            data.point_index = data.point_index + 2
            data.n = data.n + 2

    return data


# 将点按照横坐标从小到大排序
def sort_nodes(nodes_dict):
    sorted_nodes_dict = dict(sorted(nodes_dict.items(), key=lambda item: item[1]))
    sorted_nodes_list = list(sorted_nodes_dict.keys())
    return sorted_nodes_list


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
                        if len(get_hashable_cycle(cycle_stack[i:])) <= 6 and len(
                                get_hashable_cycle(cycle_stack[i:])) != 3:
                            return False

            except StopIteration:
                stack.pop()
                cycle_stack.pop()

    return True


# 判断是否可以连边，不出现C6
def is_con_edges(data, source=None):
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
                            return False

            except StopIteration:
                stack.pop()
                cycle_stack.pop()

    return True


# 从一点开始找到某一固定长度路径的其他点(一对)
def find_fixed_len_points_one(data, point, length):
    points = set()
    for nn in data.G.nodes():
        if point != nn:
            paths = nx.all_shortest_paths(data.G, point, nn)
            for path in paths:
                if len(path) == length:
                    points.add(nn)

    return points


# 从一点开始找到某一固定长度路径的其他点(两对）
def find_fixed_len_points_two(data, point, length):
    points = set()
    for nn in data.G.nodes():
        if data.G.nodes[nn]['point_num'] == 0 and point != nn:
            paths = nx.all_shortest_paths(data.G, point, nn)
            for path in paths:
                if len(path) == length:
                    points.add(nn)

    return points


# 从一点开始找到某一固定长度路径的其他点(四对)
def find_fixed_len_points_four(data, point, length):
    points = set()
    for nn in data.G.nodes():
        if data.G.nodes[nn]['point_num'] == 0 and point != nn:
            paths = nx.all_shortest_paths(data.G, point, nn)
            for path in paths:
                if len(path) == length:
                    points.add(nn)

    return points


# 获取point_num为0的点
def get_useful_points(data):
    left_useful_point = []
    for point in data.G.nodes():
        if data.G.nodes[point]['point_num'] == 0:
            left_useful_point.append(point)

    return left_useful_point


# 获取图的剩余顶点
def get_graph_points(data):
    left_graph_point = []
    x = -0.5
    y = -2.5
    for _ in range(data.n):
        data.G.add_node(data.point_index, point_num=0, position=(x, y))
        x += 0.5
        left_graph_point.append(data.point_index)
        data.point_index += 1

    return data, left_graph_point


# 将十进制转化成二进制
def dec2bin(dec):
    bin_result = ''
    if dec:
        bin_result = dec2bin(dec // 2)
        bin_result += str(dec % 2)
    else:
        bin_result = bin_result
    return bin_result


# 将二进制长度固定为可用点个数
def add_len(bin_result, bin_len):
    added_result = bin_result
    if len(bin_result) != bin_len:
        for time in range(bin_len - len(bin_result)):
            added_result = '0' + added_result

    return added_result


# 得到所有可能连接的情况
def get_con_list(left_useful_points):
    result_lists = []
    bin_len = len(left_useful_points)
    for time in range(1, 2 ** bin_len):
        bin_result = dec2bin(time)
        added_result = add_len(bin_result, bin_len)
        result_lists.append(list(added_result))

    return result_lists


# 得到所有可能连接情况的点
def get_con_point_list(con_list, left_useful_point):
    con_point_list = []
    for con_one_list in con_list:
        useful_index = 0
        temp_list = []
        for con in con_one_list:
            if int(con) == 1:
                temp_list.append(left_useful_point[useful_index])
                useful_index += 1
            else:
                useful_index += 1
        con_point_list.append(temp_list)

    return con_point_list


# 剩余点中的一个点连接所有可用点
def graph_con_usefuls(data, con_point_list, graph_point):
    for con_point in sorted(con_point_list, key=lambda i: len(i), reverse=True):
        for point_index in range(len(con_point)):
            data.G.add_edge(graph_point, con_point[point_index], edge_num=0)
            data.edge += 1
        if is_con_edges(data):
            data.n -= 1
            break
        else:
            for point_index in range(len(con_point)):
                data.G.remove_edge(graph_point, con_point[point_index])
                data.edge -= 1

    return data


def find_useful_point(node, useful_points):
    for point in useful_points:
        if node in point:
            point.remove(node)


def sort_list(useful_point):
    n = len(useful_point)
    for x in range(n - 1):
        for y in range(n - 1 - x):
            if useful_point[y] > useful_point[y + 1]:
                useful_point[y], useful_point[y + 1] = useful_point[y + 1], useful_point[y]

    return useful_point


def reset_useful_point(useful_point, sys_dict):
    new_useful_point = []
    temp_useful_point = []
    for point in useful_point:
        if len(point) != 0:
            if point[0] in sys_dict:
                if point[0] != sys_dict[point[0]]:
                    new_useful_point.append(point)
                    if [sys_dict[point[0]]] in useful_point:
                        new_useful_point.append([sys_dict[point[0]]])
                        useful_point.remove([sys_dict[point[0]]])
                else:
                    temp_useful_point.append(point)
            else:
                temp_useful_point.append(point)

    temp_useful_point = sort_list(temp_useful_point)
    for point in temp_useful_point:
        new_useful_point.append(point)

    return new_useful_point


# 添加四对虚点
def four_pairs(n):
    G = None
    edge = 0
    point_index = 9
    sys_dict = {1: 1, 2: 8, 3: 7, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2}
    useful_point = []
    data = Data(G, n, edge, point_index, sys_dict, useful_point)

    data = add_four_pairs(data)

    data_que = Queue()
    data_que.put(data)

    results_data = []

    while not data_que.empty():
        cur_data = data_que.get()
        if cur_data.n != 0:
            if len(cur_data.useful_point) != 0:
                if len(cur_data.useful_point[0]) == 1 or len(cur_data.useful_point[0]) == 0:
                    cur_data.useful_point = sort_list(cur_data.useful_point)
                    cur_data.useful_point = reset_useful_point(cur_data.useful_point, cur_data.sys_dict)
                usefulpoint = cur_data.useful_point[0]
                cur_data.useful_point.remove(usefulpoint)
                if len(usefulpoint) == 2:
                    # is_deal, data, data1, data2 = connect_sys_points(cur_data, usefulpoint[0], usefulpoint[1])
                    # if is_deal:
                    #     if data.n != data1.n:
                    #         if data1.n == 0:
                    #             results_data.append(data1)
                    #         else:
                    #             data_que.put(data1)
                    #     if data.n != data2.n:
                    #         if data2.n == 0:
                    #             results_data.append(data2)
                    #         else:
                    #             data_que.put(data2)
                    #     print('该对对称点在一对对称点之间处理完成')
                    # else:
                    is_deal1, dataa, data11, data21 = connect_no_sys_point_p6_four(cur_data, usefulpoint[0],
                                                                                   usefulpoint[1])
                    if is_deal1:
                        if dataa.n != data11.n:
                            if data11.n == 0:
                                results_data.append(data11)
                            else:
                                data_que.put(data11)
                        if dataa.n != data21.n:
                            if data21.n == 0:
                                results_data.append(data21)
                            else:
                                data_que.put(data21)
                        print('该对对称点在一对对称点与其他点P6之间处理完成')
                    else:
                        is_deal2, datab, data12, data22 = connect_no_sys_point_p5_four(cur_data, usefulpoint[0],
                                                                                       usefulpoint[1])
                        if is_deal2:
                            if datab.n != data12.n:
                                if data12.n == 0:
                                    results_data.append(data12)
                                else:
                                    data_que.put(data12)
                            if datab.n != data22.n:
                                if data22.n == 0:
                                    results_data.append(data22)
                                else:
                                    data_que.put(data22)
                            print('该对对称点在一对对称点与其他点P5之间处理完成')
                        else:
                            cur_data.useful_point.append([usefulpoint[0]])
                            cur_data.useful_point.append([usefulpoint[1]])
                            data_que.put(cur_data)

                if len(usefulpoint) == 1:
                    if len(usefulpoint) != 0:
                        if usefulpoint[0] in cur_data.G.nodes():
                            datac, data13, data23, data33, data43, data51 = connect_no_sys_point_four(cur_data,
                                                                                                      usefulpoint[0])
                            flag = False
                            if datac.n != data13.n:
                                flag = True
                                if data13.n == 0:
                                    results_data.append(data13)
                                else:
                                    data_que.put(data13)
                            if datac.n != data23.n:
                                flag = True
                                if data23.n == 0:
                                    results_data.append(data23)
                                else:
                                    data_que.put(data23)
                            if datac.n != data33.n:
                                flag = True
                                if data33.n == 0:
                                    results_data.append(data33)
                                else:
                                    data_que.put(data33)
                            if datac.n != data43.n:
                                flag = True
                                if data43.n == 0:
                                    results_data.append(data43)
                                else:
                                    data_que.put(data43)
                            if datac.n != data51.n:
                                flag = True
                                if data51.n == 0:
                                    results_data.append(data51)
                                else:
                                    data_que.put(data51)

                            if not flag:
                                results_data.append(cur_data)

                if len(cur_data.useful_point) != 0:
                    if cur_data.n != 0:
                        data_que.put(cur_data)
                results_data.append(cur_data)
        else:
            results_data.append(cur_data)

    G = None
    edge = 0
    point_index = 9
    sys_dict = {1: 1, 2: 8, 3: 7, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2}
    useful_point = []
    data = Data(G, n, edge, point_index, sys_dict, useful_point)

    data = add_four_pairs(data)

    data_que = Queue()
    data_que.put(data)

    results_data = []

    while not data_que.empty():
        cur_data = data_que.get()
        if cur_data.n != 0:
            if len(cur_data.useful_point) != 0:
                if len(cur_data.useful_point[0]) == 1 or len(cur_data.useful_point[0]) == 0:
                    cur_data.useful_point = sort_list(cur_data.useful_point)
                    cur_data.useful_point = reset_useful_point(cur_data.useful_point, cur_data.sys_dict)
                usefulpoint = cur_data.useful_point[0]
                cur_data.useful_point.remove(usefulpoint)
                if len(usefulpoint) == 2:
                    # is_deal, data, data1, data2 = connect_sys_points(cur_data, usefulpoint[0], usefulpoint[1])
                    # if is_deal:
                    #     if data.n != data1.n:
                    #         if data1.n == 0:
                    #             results_data.append(data1)
                    #         else:
                    #             data_que.put(data1)
                    #     if data.n != data2.n:
                    #         if data2.n == 0:
                    #             results_data.append(data2)
                    #         else:
                    #             data_que.put(data2)
                    #     print('该对对称点在一对对称点之间处理完成')
                    # else:
                    is_deal2, datab, data12, data22 = connect_no_sys_point_p5_four(cur_data, usefulpoint[0],
                                                                                   usefulpoint[1])
                    if is_deal2:
                        if datab.n != data12.n:
                            if data12.n == 0:
                                results_data.append(data12)
                            else:
                                data_que.put(data12)
                        if datab.n != data22.n:
                            if data22.n == 0:
                                results_data.append(data22)
                            else:
                                data_que.put(data22)
                        print('该对对称点在一对对称点与其他点P5之间处理完成')
                    else:
                        is_deal1, dataa, data11, data21 = connect_no_sys_point_p6_four(cur_data, usefulpoint[0],
                                                                                       usefulpoint[1])
                        if is_deal1:
                            if dataa.n != data11.n:
                                if data11.n == 0:
                                    results_data.append(data11)
                                else:
                                    data_que.put(data11)
                            if dataa.n != data21.n:
                                if data21.n == 0:
                                    results_data.append(data21)
                                else:
                                    data_que.put(data21)
                            print('该对对称点在一对对称点与其他点P6之间处理完成')
                        else:
                            cur_data.useful_point.append([usefulpoint[0]])
                            cur_data.useful_point.append([usefulpoint[1]])
                            data_que.put(cur_data)

                if len(usefulpoint) == 1:
                    if len(usefulpoint) != 0:
                        if usefulpoint[0] in cur_data.G.nodes():
                            datac, data13, data23, data33, data43, data51 = connect_no_sys_point_four(cur_data,
                                                                                                      usefulpoint[0])
                            flag = False
                            if datac.n != data13.n:
                                flag = True
                                if data13.n == 0:
                                    results_data.append(data13)
                                else:
                                    data_que.put(data13)
                            if datac.n != data23.n:
                                flag = True
                                if data23.n == 0:
                                    results_data.append(data23)
                                else:
                                    data_que.put(data23)
                            if datac.n != data33.n:
                                flag = True
                                if data33.n == 0:
                                    results_data.append(data33)
                                else:
                                    data_que.put(data33)
                            if datac.n != data43.n:
                                flag = True
                                if data43.n == 0:
                                    results_data.append(data43)
                                else:
                                    data_que.put(data43)
                            if datac.n != data51.n:
                                flag = True
                                if data51.n == 0:
                                    results_data.append(data51)
                                else:
                                    data_que.put(data51)

                            if not flag:
                                results_data.append(cur_data)

                if len(cur_data.useful_point) != 0:
                    if cur_data.n != 0:
                        data_que.put(cur_data)
                results_data.append(cur_data)
        else:
            results_data.append(cur_data)

    return results_data


if __name__ == '__main__':
    for point in range(32, 51):
        results_data = four_pairs(point)

        print(len(results_data))

        results_data_dict = {results_data[0].n: results_data[0]}
        for res in results_data:
            if res.n in results_data_dict.keys():
                if res.edge > results_data_dict[res.n].edge:
                    results_data_dict[res.n] = res
            else:
                results_data_dict[res.n] = res

        i = 0
        for res_data in results_data_dict.items():
            if res_data[1].n <= 6:
                left_useful_points = get_useful_points(res_data[1])
                data, left_graph_points = get_graph_points(res_data[1])
                con_lists = get_con_list(left_useful_points)
                con_point_lists = get_con_point_list(con_lists, left_useful_points)
                for graph_point in left_graph_points:
                    data = graph_con_usefuls(data, con_point_lists, graph_point)
                    left_useful_points.append(graph_point)
                    con_lists = get_con_list(left_useful_points)
                    con_point_lists = get_con_point_list(con_lists, left_useful_points)

                print('point_number: %d, edge_number: %d' % (data.n, data.edge))
                i += 1
                pos = nx.get_node_attributes(data.G, 'position')
                nx.draw(data.G, with_labels=True, pos=pos)
                plt.savefig('./img4/%d_%d_%d.png' % (point, i, data.edge))
                plt.close()

        print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())))
