import ast
import re

from algorithm.charactermatch import word_match
from lattices.asttype import ast_type
from utils.fileio import load_json
from models.sentencenode import SuspectedSentenceNode


def go_split(s, symbol):
    result = [s]
    for i in symbol:
        median = []
        for z in map(lambda x: x.split(i), result):
            median.extend(z)

            # 以上三个方法都可以解决问题
        result = median
    return [x.replace(' ', '') for x in result if x not in [':\n', '']]


def get_params(node, node_params=None):
    if not node_params:
        node_params = []
    if isinstance(node, ast.Name):
        node_params.append(node.id)
        return node_params
    elif isinstance(node, ast.Call):
        for arg in node.args:
            if isinstance(arg, ast.Name):
                node_params.append(arg.id)
            else:
                node_params = get_params(arg, node_params)
    elif isinstance(node, ast.List) or isinstance(node, ast.Tuple) or isinstance(node, ast.Set):
        for arg in node.elts:
            if isinstance(arg, ast.Name):
                node_params.append(arg.id)
            else:
                node_params = get_params(arg, node_params)
    else:
        pass
    return node_params


def get_script(node, script_list):
    script_ori = script_list[node.lineno - 1:node.end_lineno]
    script_tmp = ""
    if node.__class__ in ast_type:
        for i in range(len(script_ori)):
            if ":" not in script_ori[i]:
                script_tmp = script_tmp + script_ori[i].replace('\\\n', '').replace('\n', '')
            else:
                script_tmp = script_tmp + script_ori[i]
                break
    else:
        script_tmp = "".join(script_ori).replace('\\\n', '').replace('\n', '')

    return script_tmp, go_split(script_tmp, '()[]{},=+-*/#&@!^ ')


def match_data_type(script, data_type):
    private_word_list = []

    for word in script:
        for key in data_type.keys():
            word_std_list = data_type[key]['abbr']
            if word_match(word_std_list, word):
                private_word_list.append((key, word))
    return private_word_list


def match_purpose_type(script, purpose_dict):
    purpose = "Usage"
    for word in script:
        for key in purpose_dict.keys():
            purpose_list = purpose_dict[key]['abbr']
            if word_match(purpose_list, word):
                purpose = purpose_dict[key]['path']
    return purpose


class FuncNode:
    def __init__(self, func_node, file_path, script_list=None):
        self.func_node = func_node
        self.file_path = file_path
        self.script_list = script_list
        self.private_info = []
        self.key_variable = {}
        self.func_name = func_node.name

    def get_flow_nodes(self, node):
        pass

    def get_sentence_nodes(self, node=None, all_nodes=None):
        if node is None:
            node = self.func_node
        if all_nodes is None:
            all_nodes = []

        line_no = node.lineno

        script_ori, script = get_script(node, self.script_list)

        data_type = load_json('lattices/datatype.json')
        purpose_dict = load_json('lattices/purpose.json')

        private_word_list = match_data_type(script, data_type)
        purpose = "Usage"

        if len(private_word_list) > 0:
            purpose = match_purpose_type(script, purpose_dict)
            sentence_node = SuspectedSentenceNode(self.file_path, line_no, private_word_list, purpose, script_ori)
            all_nodes.append(sentence_node)

            # print(self.file_path, line_no)
            # print(script_ori)
            # print(script)
            # print("private_word: ", private_word_list)
            # print(purpose)
            # print()

        for private_word in private_word_list:
            if private_word[0] not in [info[0] for info in self.private_info]:
                self.private_info.append((private_word[0], purpose))

        node_son_list = None
        # print(script_ori)
        for field, value in ast.iter_fields(node):
            # print(field, value)
            if field == "body":
                node_son_list = value
            # if isinstance(value, ast.Call):
            #     print("asdfasdfadfasdf:", value.func.attr)
            # if field == "targets":
            #     if len(private_word_list) > 0:
            #         pass

        # print("添加前", all_nodes)
        if isinstance(node, ast.Assign):
            if len(private_word_list) > 0:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.key_variable[target.id] = (private_word_list, purpose)
                    elif isinstance(target, ast.Attribute):
                        self.key_variable[target.attr] = (private_word_list, purpose)
                    else:
                        pass
            else:
                node_params = get_params(node.value)
                for node_param in node_params:
                    if node_param in list(self.key_variable.keys()):
                        private_word_list_inherit, purpose_inherit = self.key_variable[node_param]
                        sentence_node = SuspectedSentenceNode(self.file_path, line_no,
                                                              private_word_list_inherit,
                                                              purpose_inherit, script_ori)
                        all_nodes.append(sentence_node)
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                self.key_variable[target.id] = (private_word_list_inherit, purpose_inherit)
                            elif isinstance(target, ast.Attribute):
                                self.key_variable[target.attr] = (private_word_list_inherit, purpose_inherit)
                            elif isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name):
                                self.key_variable[target.value.id] = (private_word_list_inherit, purpose_inherit)
                            else:
                                pass
                            # self.key_variable[target.id] = (private_word_list_inherit, purpose_inherit)

        elif isinstance(node, ast.Expr):
            node_params = get_params(node.value)
            if len(node_params) > 0:
                for node_param in node_params:
                    if node_param in list(self.key_variable.keys()) and len(private_word_list) == 0:
                        private_word_list_inherit, purpose_inherit = self.key_variable[node_param]
                        sentence_node = SuspectedSentenceNode(self.file_path, line_no,
                                                              private_word_list_inherit,
                                                              purpose_inherit, script_ori)
                        all_nodes.append(sentence_node)
        # print("添加后", all_nodes)

        if node_son_list is not None:
            for node_son in node_son_list:
                all_nodes = self.get_sentence_nodes(node_son, all_nodes)
        return all_nodes

    def __str__(self):
        return self.script_list[0]
