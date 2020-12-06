import hashlib
import re
import pynauty as nu
from pynauty import certificate


def get_info(G):
    """
    打印图 G 的信息
    :param G:
    :return:
    """
    print(G.number_of_vertices)
    print(G)
    print("=-"*20)


def get_file(file_name):
    """
    读取文件，获取图信息
    :param file_name: 文件名
    :return:
    """
    f = open(file_name, "r")
    data = f.readlines()
    f.close()
    return data


if __name__ == '__main__':
    data = get_file("set.txt")

    # 删掉头部Set字符
    for i in range(len(data)):
        data[i] = data[i].strip('Set')

    li = []
    for j in range(len(data)):
        # 定义顶点数为11 的图
        G = nu.Graph(11)
        # 获取data中顶点间 边的关系
        edge = [int(s) for s in re.findall(r'\b\d+\b', data[j])]
        # 连边
        for x in range(0, len(edge) - 1, 2):
            G.connect_vertex(edge[x] - 1, edge[x + 1] - 1)
        li.append(G)
        get_info(G)

    # 两两判同构
    print(nu.isomorphic(li[0], li[1]))

    a = certificate(li[0])
    a1 = certificate(li[1])

    b = hashlib.sha256(a)
    b1 = hashlib.sha256(a1)
    print(b.hexdigest())
    print(b1.hexdigest())



