from GraphEch import *

result_graph = None


@count_time()
def make_graph(graphs):
    """
    绘制图
    :param graph_c: 图
    """
    global result_graph
    result_graph = graphs[0]

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
                    else:
                        add_12(graph_c, edge)

                elif graph_c.remain_points == 2:
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
        if graph_c.edge >= result_graph.edge:
            # if graph_c.point_index <= result_graph.point_index:
            result_graph = graph_c

    return deepcopy(result_graph)


@count_time("The total time： ")
def run():
    path = "img"
    mkdir(path)
    for points in range(28, 50):

        # graph = GraphC7()

        graph_four = GraphC8(points)
        graph_four.init_four()

        graph_three = GraphC8(points)
        graph_three.init_three()

        graph_two = GraphC8(points)
        graph_two.init_two()

        graph_one = GraphC8(points)
        graph_one.init_one()

        graphs = [graph_four, graph_three, graph_two, graph_one]
        # graphs = [graph_two, ]

        graph = make_graph(graphs)
        print(result_graph)
        save_graph(points, result_graph, path=path)


if __name__ == '__main__':
    run()
