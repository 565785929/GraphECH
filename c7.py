from GraphEch import *
import time
result_graph = None
result_gs = None

graph_set = set()

def isomorphism(g):
    gc = get_graph_ceritficate(g)
    if gc in graph_set:
        return True
    else:
        graph_set.add(gc)
        # print("isomorphism------graph:", g.G.edges)
        return False


@count_time()
def make_graph(graphs):
    """
    绘制图
    :param graph_c: 图
    """
    global result_graph
    global result_gs

    result_graph = graphs[0]
    result_gs = []
    while len(graphs) != 0:
        graph_c = graphs.pop(0)

        # 仍有未使用的点
        while graph_c.remain_points != 0:
            # 有可拓展的边
            while graph_c.useful_edge_length() != 0:
                if graph_c.remain_points >= 3:
                    # 拓展k5
                    add_k5(graph_c, graph_c.useful_edge.pop())
                if graph_c.remain_points == 0:
                    # 无可用点 TODO 可优化 分解四个k5
                    break
                elif graph_c.remain_points == 1:
                    # 剩余一个点 判断是否有两个相邻可用边
                    edge = graph_c.get_useful_edge()
                    # edge_point_one(graph_c, edge)
                    if len(edge) == 0:
                        continue
                    elif len(edge) == 3:
                        # TODO 可优化 分解两个k5
                        add_13(graph_c, edge)
                        graph_c.tail_point = 1
                    else:
                        add_12(graph_c, edge)
                        graph_c.tail_point = 1

                    # 拓展
                    # graph_c.one_expand()


                elif graph_c.remain_points == 2:
                    graph_c.tail_point = 2
                    edge = graph_c.get_useful_edge()
                    # edge_point_two(graph_c, edge)
                    if len(edge) == 0:
                        continue
                    elif len(edge) == 3:
                        add_k5e(graph_c, edge)
                    else:
                        add_25(graph_c, edge)

            if graph_c.useful_edge_length() == 0 and graph_c.remain_points != 0:
                # 制造可拓展边
                graphs.extend(graph_c.expand_p())
                break

        # 拓展所有p7
        graph_c.all_p7()
        bn = [0, 0, 0, 0, 0, 0, 1, 1, 2, 3, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 16, 18, 20, 21, 23, 26, 28, 30, 32, 35,
              37, 40, 43, 45, 48, 51, 54, 57, 61, 64, 67, 71, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 115, 119, 124,
              129, 133, 138, 143, 148, 153, 159, 164, 169, 175, 180, 186, 192, 198, 204, 210]

        if graph_c.edge >= result_graph.edge:
            if graph_c.edge == result_graph.edge:
                if graph_c.edge >= bn[graph_c.ppoints]:
                    if not isomorphism(graph_c):
                        result_gs.append(graph_c)

            else:
                for i in result_gs:
                    del i
                result_gs.clear()
                result_graph = graph_c

    return deepcopy(result_graph)


@count_time("The total time： ")
def run():
    path = "img_uuid"
    mkdir(path)
    for points in range(28, 74):

        g7_graph_two = GraphC7(points)
        g7_graph_two.init_two()
        g7_graph_four = GraphC7(points)
        g7_graph_four.init_four()

        g8_graph_four = GraphC8(points)
        g8_graph_four.init_four()
        g8_graph_three = GraphC8(points)
        g8_graph_three.init_three()
        g8_graph_two = GraphC8(points)
        g8_graph_two.init_two()
        g8_graph_one = GraphC8(points)
        g8_graph_one.init_one()

        g10_graph_five = GraphC10(points)
        g10_graph_five.init_five()
        g10_graph_four = GraphC10(points)
        g10_graph_four.init_four()
        g10_graph_three = GraphC10(points)
        g10_graph_three.init_three()
        g10_graph_two = GraphC10(points)
        g10_graph_two.init_two()
        g10_graph_one = GraphC10(points)
        g10_graph_one.init_one()

        graphs = [g10_graph_five, g10_graph_four, g10_graph_three, g10_graph_two, g10_graph_one, g8_graph_four,
                  g8_graph_three, g8_graph_two, g8_graph_one, g7_graph_four, g7_graph_two]
        # graphs = [graph_two, ]

        graph = make_graph(graphs)
        # print(result_graph)
        save_graph(points, result_graph, path=path)
        print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())))

        # ALL graph

        for g in result_gs:

            if g.tail_point == 1:
                g.one_expand()
            save_graph(points, g, path)


if __name__ == '__main__':
    run()

