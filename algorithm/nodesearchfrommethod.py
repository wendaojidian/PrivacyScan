import ast
import copy

from models.sentencenode import SuspectedSentenceNode


def get_func_list(node, func_list=None):
    if func_list is None:
        func_list = []
    if isinstance(node, ast.Call):
        func_list.append(node.func.id)
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


def suspected_node_search_recsec(node, func_node_dict, node_list_1st, file_name, node_list=None):
    if node_list is None:
        node_list = []
    func_list = []
    if isinstance(node, ast.Expr) or isinstance(node, ast.Assign):
        func_list = get_func_list(node.value)
    elif isinstance(node, ast.For):
        func_list = get_func_list(node.iter)
    elif isinstance(node, ast.While) or isinstance(node, ast.If):
        func_list = get_func_list(node.test)
    elif isinstance(node, ast.With):
        for item in node.items:
            func_list = get_func_list(item, func_list)

    # print("1111111111:", func_node_dict['utils.UserSession.checkUserSession'])
    if len(func_list) > 0:
        func_list = list(set(func_list))
        # print(file_name, node.lineno)
        # print(func_list)
        private_info = []
        for func in func_list:
            if func in func_node_dict.keys():
                private_info.extend(func_node_dict[func])
        if len(private_info) > 0:
            sentence_node = SuspectedSentenceNode(file_name, node.lineno, private_word_list=None, purpose=None,
                                                  private_info=private_info)
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
            node_list = suspected_node_search_recsec(node_son, func_node_dict, node_list_1st, file_name, node_list)
    except AttributeError:
        pass

    return node_list


def suspected_node_search_sec(tree_lines_files, func_node_dict, node_list_1st):
    suspected_node_list_sec = []
    func_node_dict_new = {}
    for key in func_node_dict.keys():
        if key.find('__') == -1:
            func_node_dict_new[key.split('.')[-1]] = func_node_dict[key]
    # print(func_node_dict_new)
    for tree, lines, file_name in tree_lines_files:
        suspected_node_sec = suspected_node_search_recsec(tree, func_node_dict, node_list_1st, file_name)
        suspected_node_list_sec.extend(suspected_node_sec)

    return suspected_node_list_sec

