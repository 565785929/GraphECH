from copy import deepcopy

from GraphUtil import *


class GraphC:
    def __init__(self):
        self.G = nx.Graph()
        # 边数
        self.edge = 0
        # 可用点
        self.useful_point = []
        # 点索引
        self.point_index = 1
        # 可用边
        self.useful_edge = []
        # 总点
        self.remain_points = 0
        # k5e
        self.k5e_point = []


    def useful_edge_length(self):
        """
        可用边数量
        :return:
        """
        return len(self.useful_edge)

    def get_useful_edge(self):
        """
        获取相邻可拓展边 TODO 需改进
        eg: 如果剩余[[1, 2], [2, 3]]
        则返回 [1, 2, 3]
        :return: [a, b, c]
        """
        edge = []
        if len(self.useful_edge) >= 2:
            li = []
            p = -1
            for i, j in self.useful_edge:
                li.append(i)
                li.append(j)
                li.sort()
            for k in range(len(li)-1):
                if li[k] == li[k+1]:
                    p = li[k]
            if p == -1:
                return self.useful_edge.pop()
            # 拼接[a, b, c]
            for i, j in self.useful_edge:
                if i == p:
                    edge.append(j)
                elif j == p:
                    edge.append(i)
                if len(edge) == 2:
                    edge.insert(1, p)
            return edge
        elif len(self.useful_edge) != 0:
            return self.useful_edge.pop()
        else:
            return edge

    def expand_p(self):
        """
        无可用边，加点拓展
        :return:
        """
        results = self.p7()
        if self.remain_points != 0:
            if len(results) == 0:
                results = self.p6()
                if len(results) == 0:
                    results = self.p5()
                    if len(results) == 0:
                        print("=- Can't expand graph -=")
                    else:
                        print("p5")
                else:
                    print("p6")
            else:
                print("p7")

        return results

    def p7(self):
        res = []
        for source in self.useful_point:
            targets = find_len_points(self, source, 7)
            # p1 = find_fixed_len_points_one(self, p, 7)
            for target in targets:
                g = deepcopy(self)
                g.useful_edge.append((source, target))
                g.G.add_edge(source, target)
                res.append(g)
        return res

    def p6(self):
        res = []
        for source in self.useful_point:
            targets = find_len_points(self, source, 6)
            for target in targets:
                g = deepcopy(self)
                pos1 = g.G.nodes[source]['position']
                pos2 = g.G.nodes[target]['position']
                x, y = add_xpoint(pos1, pos2)
                g.G.add_node(g.point_index, point_num=0, position=(x, y))
                g.G.add_edge(source, g.point_index)
                g.G.add_edge(target, g.point_index)
                g.remain_points -= 1
                g.edge += 2
                g.useful_point.append(g.point_index)

                g_k5e = deepcopy(g)
                g_k5e.useful_edge.append((source, g.point_index))
                g_k5e.useful_edge.append((target, g.point_index))
                g_k5e.point_index += 1
                res.append(g_k5e)

                if g.remain_points >= 2:
                    g.k5e_point.append(g.point_index)
                    g.point_index += 1
                    add_k5e(g, (target, g.point_index-1, source))
                    # g.remain_points -= 2
                    # g.edge += 7
                    res.append(g)
                # show_graph(g)

        return res

    def p5(self):
        res = []
        for source in self.useful_point:
            targets = find_len_points(self, source, 5)

            for target in targets:
                g = deepcopy(self)
                pos1 = g.G.nodes[source]['position']
                pos2 = g.G.nodes[target]['position']
                x, y = (pos1[0]+pos2[0]) / 3, (pos1[1]+pos2[1]) / 3
                g.G.add_node(g.point_index, point_num=0, position=(x, y))
                g.useful_edge.append((source, g.point_index))
                g.G.add_edge(source, g.point_index)
                # add useful point
                g.useful_point.append(g.point_index)
                g.point_index += 1
                g.remain_points -= 1
                g.edge += 1
                if g.remain_points >= 1:
                    g.useful_edge.append((g.point_index - 1, g.point_index))
                    g.G.add_edge(g.point_index - 1, g.point_index)

                    x1, y1 = (pos1[0] + pos2[0]) / 3 * 2, (pos1[1] + pos2[1]) / 3 * 2

                    g.G.add_node(g.point_index, point_num=0, position=(x1, y1))
                    g.useful_edge.append((target, g.point_index))
                    g.G.add_edge(target, g.point_index)
                    g.useful_point.append(g.point_index)

                    g.point_index += 1
                    g.remain_points -= 1
                    g.edge += 2
                    res.append(g)
        return res

    def all_p7(self):
        """
        连接所有距离 >=7 的边
        :return:
        """
        p1 = find_all_p7_points(self)
        while p1 != -1:
            self.edge += 1
            self.G.add_edge(p1[0], p1[1])
            p1 = find_all_p7_points(self)
            print("=- all_p7 -=")

    def shit_method(self):
        """
        遍历所有的点，连一下试试,,, 可以dp
        :return:
        """
        nodes = self.useful_point
        edges = self.G.edges
        for source in nodes:
            for target in nodes:
                if source != target:
                    if (source, target) not in edges:
                        self.G.add_edge(source, target)
                        if not is_more_6(self):
                            self.G.remove_edge(source, target)
                        else:
                            self.edge += 1
                            return



class GraphC7(GraphC):
    def __init__(self, points):
        super().__init__()
        self.point_index = 8
        self.remain_points = points
        self.G.add_node(1, point_num=2, position=(0, 2))
        self.G.add_node(2, point_num=2, position=(1.5, 1.5))
        self.G.add_node(3, point_num=2, position=(2, 0))
        self.G.add_node(4, point_num=2, position=(1.5, -1.5))
        self.G.add_node(5, point_num=2, position=(-1.5, -1.5))
        self.G.add_node(6, point_num=2, position=(-2, 0))
        self.G.add_node(7, point_num=2, position=(-1.5, 1.5))
        self.remain_points -= 7

    def init_four(self):
        """
        初始化母图C7
        """
        for _ in range(1, 8):
            self.G.add_edge(_, _ % 7 + 1, edge_num=1)
            self.useful_edge.append((_, _ % 7 + 1))
        # self.useful_edge.append((1,2))
        # self.useful_edge.append((3,2))
        # self.useful_edge.append((3,4))
        # self.useful_edge.append((5,4))
        # self.useful_edge.append((5,6))
        # self.edge += 7
        # self.remain_points -= 2

        self.edge += 7

    def init_two(self):
        """
        初始化母图C7
        """
        for _ in range(1, 8):
            self.G.add_edge(_, _ % 7 + 1, edge_num=1)
            # self.useful_edge.append((_, _ % 7 + 1))
        self.useful_edge.append((1, 2))
        self.useful_edge.append((3, 2))
        self.useful_edge.append((3, 4))
        self.useful_edge.append((5, 4))
        self.useful_edge.append((5, 6))
        self.edge += 7
        self.remain_points -= 2

        self.edge += 7


class GraphC8(GraphC):
    def __init__(self, points):
        super().__init__()

        self.point_index = 9
        self.remain_points = points
        self.G.add_node(1, point_num=2, position=(0, 2))
        self.G.add_node(2, point_num=2, position=(1.5, 1.5))
        self.G.add_node(3, point_num=2, position=(2, 0))
        self.G.add_node(4, point_num=2, position=(1.5, -1.5))
        self.G.add_node(5, point_num=2, position=(0, -2))
        self.G.add_node(6, point_num=2, position=(-1.5, -1.5))
        self.G.add_node(7, point_num=2, position=(-2, 0))
        self.G.add_node(8, point_num=2, position=(-1.5, 1.5))
        self.remain_points -= 8

        for _ in range(1, 9):
            self.G.add_edge(_, _ % 8 + 1, edge_num=1)
        self.edge += 8

    def init_four(self):
        for _ in range(1, 9):
            self.useful_edge.append((_, _ % 8 + 1))

    def init_three(self):
        self.useful_edge.append((1, 2))
        self.useful_edge.append((3, 2))
        self.useful_edge.append((3, 4))
        self.useful_edge.append((5, 4))
        self.useful_edge.append((5, 6))
        self.useful_edge.append((7, 6))
        self.edge += 7
        self.remain_points -= 2

    def init_two(self):
        self.useful_edge.append((1, 2))
        self.useful_edge.append((3, 2))
        self.useful_edge.append((5, 6))
        self.useful_edge.append((7, 6))
        self.edge += 14
        self.remain_points -= 4

    def init_one(self):
        self.useful_edge.append((3, 4))
        self.useful_edge.append((7, 6))
        self.edge += 21
        self.remain_points -= 6
