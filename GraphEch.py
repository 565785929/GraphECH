from GraphUtil import *


class GraphC:
    def __init__(self):
        self.G = nx.Graph()
        self.edge = 0
        self.useful_point = []
        self.point_index = 1
        self.useful_edge = []
        self.remain_points = 0

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
        if not self.p7():
            if not self.p6():
                if not self.p5():
                    print("-=" * 20)
                    print("Can't expand graph")

    def p7(self):
        for p in self.useful_point:
            p1 = find_len_points(self, p, 7)
            # p1 = find_fixed_len_points_one(self, p, 7)
            if p1 != -1:
                self.useful_edge.append((p, p1))
                self.G.add_edge(p, p1)
                return True
        return False

    def p6(self):
        for p in self.useful_point:
            p1 = find_len_points(self, p, 6)
            if p1 != -1:
                pos1 = self.G.nodes[p]['position']
                pos2 = self.G.nodes[p1]['position']
                x, y = add_xpoint(pos1, pos2)
                self.G.add_node(self.point_index, point_num=0, position=(x, y))

                self.useful_edge.append((p, self.point_index))
                self.useful_edge.append((p1, self.point_index))
                self.G.add_edge(p, self.point_index)
                self.G.add_edge(p1, self.point_index)
                self.point_index += 1
                self.remain_points -= 1
                self.edge += 2
                return True
        return False

    def p5(self):
        for p in self.useful_point:
            p1 = find_len_points(self, p, 5)
            if p1 != -1:
                pos1 = self.G.nodes[p]['position']
                pos2 = self.G.nodes[p1]['position']
                x, y = (pos1[0]+pos2[0]) / 3, (pos1[1]+pos2[1]) / 3
                self.G.add_node(self.point_index, point_num=0, position=(x, y))
                self.useful_edge.append((p, self.point_index))
                self.G.add_edge(p, self.point_index)
                self.point_index += 1
                self.remain_points -= 1
                self.edge += 1
                if self.remain_points >= 1:
                    self.useful_edge.append((self.point_index - 1, self.point_index))
                    self.G.add_edge(self.point_index - 1, self.point_index)

                    x1, y1 = (pos1[0] + pos2[0]) / 3 * 2, (pos1[1] + pos2[1]) / 3 * 2

                    self.G.add_node(self.point_index, point_num=0, position=(x1, y1))
                    self.useful_edge.append((p1, self.point_index))
                    self.G.add_edge(p1, self.point_index)

                    self.point_index += 1
                    self.remain_points -= 1
                    self.edge += 2

                return True
        return False

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
            print("-=" * 50)


class GraphC7(GraphC):
    def __init__(self):
        super().__init__()

    def init_four(self, points):
        """
        初始化母图C7
        """
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

    def init_two(self, points):
        """
        初始化母图C7
        """
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
