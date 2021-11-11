import copy
import os
import re
import graphviz
import pyan


class ProjectAnalyzer:
    def __init__(self, project):
        tmpfile = "./tmp.gv"
        graghviz(tmpfile, walk_files_path(project))
        # _methods:函数名
        # _method_matrix:直接调用矩阵
        self._methods, self._method_matrix, self._clazzs = analyze_gv(tmpfile, project=project, endpoint=".py")
        # _matrix:可达性矩阵
        # _mediate:中间节点矩阵
        self._matrix = copy.deepcopy(self._method_matrix)
        self._mediate = algorithm(self._matrix)

    def get_methods(self):
        return self._methods

    def get_class(self):
        return self._clazzs

    def find_direct_call_func(self):
        result = {}
        dimension = len(self._methods)
        for i in range(dimension):
            result[self._methods[i]] = []
            for j in range(dimension):
                if self._method_matrix[i][j] > 0:
                    result[self._methods[i]].append(self._methods[j])
        return result

    def find_all_call_func(self, target_func):
        dimension = len(self._methods)
        index = self._methods.index(target_func)
        if index < 0:
            raise Exception("no such method")
        result = []
        for i in range(dimension):
            if self._matrix[index][i] > 0:
                callpath = algorithm2(self._matrix, self._mediate, index, i)
                result.append((self._methods[i], list(reversed([self._methods[x] for x in callpath]))))
        return result


def analyze_gv(gv, project="", endpoint=".py"):
    method_adjacency = []
    methods = []
    clazzs = []
    with open(gv, 'r') as gv_file:
        # 第一遍遍历找到所有的类
        for line in gv_file.readlines():
            match_group = re.search(r'([a-zA-Z0-9_]+)\s*->\s*([a-zA-Z0-9_]+)', line)
            if match_group is not None:
                # 根据类方法确定类名
                dirs = match_group.group(1).split("__")
                file = project + os.path.sep + os.path.sep.join(dirs[:len(dirs) - 2]) + endpoint
                clazz = ".".join(dirs[:len(dirs) - 1])
                is_clazz_method = os.path.isfile(file)
                if is_clazz_method and clazz not in clazzs:
                    clazzs.append(clazz)
        # 第二遍遍历找到所有的函数依赖关系
        gv_file.seek(0, 0)
        for line in gv_file.readlines():
            match_group = re.search(r'([a-zA-Z0-9_]+)\s*->\s*([a-zA-Z0-9_]+)', line)
            if match_group is not None:
                # 去除文件
                if os.path.isfile(project + os.sep + match_group.group(1).replace("__", os.sep) + endpoint):
                    # print("It's a file,skip!")
                    continue
                # 去除私有方法
                flag1 = match_group.group(1).find("____") >= 0
                if flag1:
                    continue
                flag2 = match_group.group(2).find("____") >= 0
                if flag2:
                    continue
                # 去除类
                flag3 = match_group.group(1).replace("__", ".") in clazzs or match_group.group(2).replace("__", ".") in clazzs
                if flag3:
                    continue

                if match_group.group(1) not in methods:
                    methods.append(match_group.group(1).replace("__", "."))
                if match_group.group(2) not in methods:
                    methods.append(match_group.group(2).replace("__", "."))
                method_adjacency.append((methods.index(match_group.group(2).replace("__", ".")),
                                         methods.index(match_group.group(1).replace("__", "."))))

    method_num = len(methods)
    method_matrix = [[0] * method_num for _ in range(method_num)]
    for adjacency in method_adjacency:
        method_matrix[adjacency[0]][adjacency[1]] = 1
    return methods, method_matrix, clazzs


"""
matrix1:原始矩阵(直接调用关系)
return:中间节点矩阵
"""


def algorithm(matrix):
    # 可达性矩阵
    dimension = len(matrix)
    # 中间节点矩阵
    mediate_matrix = [[0] * dimension for _ in range(dimension)]
    # n三次方次迭代
    for i in range(dimension):
        for j in range(dimension):
            if matrix[j][i] > 0:
                for k in range(dimension):
                    if matrix[j][k] == 0 and matrix[i][k] > 0:
                        matrix[j][k] = 1
                        mediate_matrix[j][k] = i
    return mediate_matrix


"""
matrix1:可达性矩阵
matrix2:中间节点矩阵
return:可达路径(包括起点终点)
"""


def algorithm2(matrix1, matrix2, start, end):
    if matrix1[start][end] == 0:
        # 不可达
        return ()
    else:
        mediate = matrix2[start][end]
        if mediate == 0:
            # 可达，无中间节点
            return start, end
        # 可达，有中间节点
        left = list(algorithm2(matrix1, matrix2, start, mediate))
        right = list(algorithm2(matrix1, matrix2, mediate, end))
        left.pop()
        left.extend(right)
        return left


def test_algorithm():
    matrix = [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
    algorithm(matrix)
    print(matrix)


def graghviz(output, args: list):
    res = pyan.create_callgraph(args, format="dot")
    graph = graphviz.Source(res)
    graph.view(filename=output)


def walk_files_path(path, endpoint='.py'):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(endpoint):
                file_list.append(file_path)
    return file_list


if __name__ == '__main__':
    p = ProjectAnalyzer("/Users/liufan/program/PYTHON/SAP/cmdb-python-master")
    print(p.get_class())
    for m in p.get_methods():
        print(m, p.find_all_call_func(m))
