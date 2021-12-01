import ast
import copy

from models.funcnode import get_script
from models.sentencenode import SuspectedSentenceNode


def get_func_list(node, func_list=None):
    if func_list is None:
        func_list = []
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute):
            func_list.append(node.func.attr)
        elif isinstance(node.func, ast.Name):
            func_list.append(node.func.id)
        if len(node.args) > 0:
            for arg in node.args:
                func_list = get_func_list(arg, func_list)
    elif isinstance(node, ast.List) or isinstance(node, ast.Tuple) or isinstance(node, ast.Set):
        for arg in node.elts:
            func_list = get_func_list(arg, func_list)
    elif isinstance(node, ast.Compare):
        for comp in node.comparators:
            func_list = get_func_list(comp, func_list)
        func_list = get_func_list(node.left, func_list)
    elif isinstance(node, ast.withitem):
        func_list = get_func_list(node.context_expr)
    return func_list


def suspected_node_search_recsec(node, lines, func_node_dict, node_list_1st, file_name, node_list=None):
    if node_list is None:
        node_list = []
    func_list = []
    if isinstance(node, ast.Expr) or isinstance(node, ast.Assign) or isinstance(node, ast.Return):
        func_list = get_func_list(node.value)
    elif isinstance(node, ast.For):
        func_list = get_func_list(node.iter)
    elif isinstance(node, ast.While) or isinstance(node, ast.If):
        func_list = get_func_list(node.test)
    elif isinstance(node, ast.With):
        for item in node.items:
            func_list = get_func_list(item, func_list)

    if len(func_list) > 0:
        confidence = 1
        func_list = list(set(func_list))
        # print(func_list)

        private_info = []
        for func in func_list:
            if func in func_node_dict.keys():
                # print(func, func_node_dict[func])
                private_info.extend(func_node_dict[func]['privacy'])
                confidence = 1/func_node_dict[func]['num']
        script = get_script(node, lines)
        # print(script)
        if len(private_info) > 0:
            # print(private_info)
            sentence_node = SuspectedSentenceNode(file_name, node.lineno, private_word_list=None, purpose=None,
                                                  private_info=private_info, script=script, confidence=confidence)
            # print(sentence_node)
            has = False
            for node_1st in node_list_1st:
                # print(node_1st)
                if sentence_node == node_1st:
                    has = True
                    break
            if not has:
                # print(sentence_node)
                node_list.append(sentence_node)
    try:
        for node_son in node.body:
            node_list = suspected_node_search_recsec(node_son, lines, func_node_dict, node_list_1st, file_name, node_list)
    except AttributeError:
        pass

    return node_list


def suspected_node_search_sec(tree_lines_files, func_node_dict, node_list_1st):
    suspected_node_list_sec = []
    for tree, lines, file_name in tree_lines_files:
        suspected_node_sec = suspected_node_search_recsec(tree, lines, func_node_dict, node_list_1st, file_name)
        suspected_node_list_sec.extend(suspected_node_sec)

    return suspected_node_list_sec

