import networkx as nx


class Gra(object):
    G = nx.Graph()
    # 边数
    __edge = 0
    # 点索引
    __index = 1
    # 可用点
    useful_point = []
    # 可用边
    useful_edge = []
    # k5e
    k5e_point = []
    # 尾点个数
    tail_point = 0

    def __init__(self, remain_points):
        # 剩余点
        self.remain_points = remain_points

    @property
    def edge(self):
        return self.__edge

    @edge.setter
    def edge(self, edge):
        self.__edge = edge

    @property
    def index(self):
        return self.__index

    def add_index(self, n=1):
        self.__index += n
        return self.index()


class Run(object):
    __graphs = []

    def __init__(self, path="img"):
        self.path = path
        pass

    def 构造(self, v, points):
        """
        构造母图，if=7，8，9，10
        :return:
        """
        self.G.add_node()
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

        for _ in range(1, v):
            self.G.add_edge(_, _ % v + 1, edge_num=1)
        self.edge += v
        pass

    def mkdir(self):
        """
        构造文件夹，准备工作
        :return:
        """
        import os
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def 队列pop(self):
        pass

    @property
    def graphs(self):
        return self.__graphs

    def run(self):
        self.__graphs.append()

    def 母图拓展(self):
        """
        c7 c8 可以放在一起
        :return:
        """
        pass


if __name__ == '__main__':
    path = "img"

    main = Run(path, )
    main.mkdir()
    main.母图拓展()
    main.入队列()
