def func_link(func_name, func_graph):
    """
    从一个方法，找到所有调用该方法的函数（包括所有层级）
    :param func_name: 方法名称
    :param func_graph: 方法依赖图（字典）
    :return: 所有调用该方法的函数（不重复，包括单层和多层）
    """
    func_all = []
    # func_all = [(func1,[func1,func2,func3,func_name]), (func2,[func2, func_name])]
    return func_all
