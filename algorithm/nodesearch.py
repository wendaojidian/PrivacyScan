import ast
from configparser import ConfigParser

from lattices.asttype import ast_type
from models.funcnode import FuncNode
from utils.fileio import load_json


def judge_node(node, file_name, script):
    print("-----------------------------------")
    print(file_name)
    print(node)
    print(script)
    # if isinstance(node, ast.)
    # 1. 判断注释
    # 2. 判断代码块初始语句
    if node.__class__ in ast_type:
        script_tmp = ""
        for i in range(len(script)):
            if ":" not in script[i]:
                script_tmp = script_tmp + script[i].replace('\\\n', '')
            else:
                script_tmp = script_tmp + script[i]
                break
        script = script_tmp
    # 3. 判断方法
    # 4. 判断类
    # 5. 判断隐私数据
    private_data = load_json("../lattices/datatype.json")

    return True


def suspected_node_search_recursion(node, file_name, script_list, node_list=None, func_node_list=None, class_name=None):
    if func_node_list is None:
        func_node_list = {}
    if node_list is None:
        node_list = []
    if isinstance(node, ast.FunctionDef):
        func_node = FuncNode(node, file_name, script_list)
        try:
            all_nodes = func_node.get_sentence_nodes()
        except AttributeError:
            raise AttributeError(file_name, node.lineno)
        node_list.extend(all_nodes)
        if len(func_node.private_info) > 0:
            cp = ConfigParser()
            cp.read("initparams.cfg", encoding='utf-8')
            source_dir = cp.get('file_absolute_path', 'source_dir')
            func_path = ""
            if class_name is None:
                func_path = func_node.file_path.replace(source_dir + '/', '').replace('.py',
                                                                                      '/' + func_node.func_name).replace(
                    '/', '.')
            else:
                func_path = func_node.file_path.replace(source_dir + '/', '').replace('.py',
                                                                                      '/' + class_name + "/" + func_node.func_name).replace('/', '.')
            func_node_list[func_path] = func_node.private_info
    elif isinstance(node, ast.ClassDef):
        class_name = node.name
        for node_son in node.body:
            if isinstance(node_son, ast.FunctionDef):
                node_list, func_node_list = suspected_node_search_recursion(node_son, file_name, script_list, node_list,
                                                                            func_node_list, class_name)
    try:
        for node_son in node.body:
            node_list, func_node_list = suspected_node_search_recursion(node_son, file_name, script_list, node_list,
                                                                        func_node_list)
    except AttributeError:
        pass

    return node_list, func_node_list


def suspected_node_search_from_files(tree_lines):
    suspected_node_list = []
    func_node_dict = {}
    for tree, lines, file_name in tree_lines:
        node_list, func_node_list = suspected_node_search_recursion(tree, file_name, lines, func_node_list=func_node_dict)
        suspected_node_list.extend(node_list)
    # print(len(suspected_node_list), len(func_node_dict.keys()))

    # for node in suspected_node_list:
    #     print(node)

    return suspected_node_list, func_node_dict
