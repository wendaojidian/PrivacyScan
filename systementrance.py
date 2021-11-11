import ast
from configparser import ConfigParser

from accuracy.accuracytest import test_recall
from utils import fileio
from algorithm.nodesearch import suspected_node_search_from_files
import numpy \
    as np

# from utils.funclink import ProjectAnalyzer
from utils.funclink import ProjectAnalyzer


def main(source):
    # step1: 读取文件
    file_list = fileio.walk_files(source)

    # 构建ast树
    suspected_node_list, func_node_dict = suspected_node_search_from_files(file_list)
    # print(len(suspected_node_list))

    for node in suspected_node_list:
        print(node)
    print(func_node_dict)
    # print(suspected_node_list, func_node_dict)

    # test_recall(suspected_node_list, source)

    # p = ProjectAnalyzer(source_dir)
    # for method in func_node_dict.keys():
    #     try:
    #         print(method, p.find_all_call_func(method))
    #     except ValueError:
    #         pass


def main2(source_file):
    file_list = [open(source_file, encoding='utf-8')]
    suspected_node_list, func_node_dict = suspected_node_search_from_files(file_list)


if __name__ == '__main__':
    cp = ConfigParser()
    cp.read("initparams.cfg", encoding='utf-8')
    source_dir = cp.get('file_absolute_path', 'source_dir')
    main(source_dir)
    # source_file = "/Users/liufan/program/PYTHON/SAP/PrivacyScan/test.py"
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