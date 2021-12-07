import ast
import copy
from configparser import ConfigParser

from accuracy.accuracytest import test_recall_accuracy
from algorithm.nodesearchfrommethod import suspected_node_search_sec
from analyze.outanalyze import out_analyze
from utils import fileio
from algorithm.nodesearch import suspected_node_search_from_files
import numpy \
    as np

# from utils.funclink import ProjectAnalyzer
from utils.funclink import ProjectAnalyzer, get_link
import time


def main(source):
    # step1: 读取文件
    file_list = fileio.walk_files(source)

    # tree_lines_files为（py文件字符串，根结点，文件名）三元组列表
    tree_lines_files = []
    for file in file_list:
        lines = file.readlines()
        tree = ast.parse(''.join(lines))
        tree_lines_files.append((tree, lines, file.name))

    # 构建ast树
    suspected_node_list, func_node_dict = suspected_node_search_from_files(tree_lines_files)

    # 递归获取所有方法可能的隐私数据和操作
    func_node_dict_all = get_link(func_node_dict, source)

    p = ProjectAnalyzer(source)

    # 第二次遍历，找到所有通过调用方法产生的隐私数据操作。
    suspected_node_list_sec = suspected_node_search_sec(tree_lines_files, func_node_dict_all, suspected_node_list,
                                                        source_dir, p)

    suspected_node_list.extend(suspected_node_list_sec)

    test_recall_accuracy(suspected_node_list, source)
    out_analyze(suspected_node_list, source)


def main2(source_file):
    file_list = [open(source_file, encoding='utf-8')]

    tree_lines_files = []
    for file in file_list:
        lines = file.readlines()
        tree = ast.parse(''.join(lines))
        tree_lines_files.append((tree, lines, file.name))
    suspected_node_list, func_node_dict = suspected_node_search_from_files(tree_lines_files)
    for node in suspected_node_list:
        print(node)
    print(func_node_dict)


if __name__ == '__main__':
    cp = ConfigParser()
    cp.read("initparams.cfg", encoding='utf-8')
    source_dir = cp.get('file_absolute_path', 'source_dir')
    time_start = time.time()
    main(source_dir)
    print(time.time() - time_start)
    # source_file = "/Users/liufan/program/PYTHON/SAP/cmdb-python-master/cmdb/views/dao/userInfoDao.py"
    # main2(source_file)

"""
<class 'ast.Expr'>,
<class 'ast.FunctionDef'>,
<class 'ast.AugAssign'>,
<class 'ast.Assign'>,
<class 'ast.ImportFrom'>,
<class 'ast.If'>,
<class 'ast.Import'>,
<class 'ast.ClassDef'>,
<class 'ast.Try'>
"""
