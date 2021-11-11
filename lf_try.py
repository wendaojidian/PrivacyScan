from IPython.display import HTML

import json

# import graphviz
# import pyan
#
# root_dir1 = "/Users/liufan/program/PYTHON/SAP/PrivacyScan/systementrance.py"
# root_dir2 = "/Users/liufan/program/PYTHON/SAP/PrivacyScan/utils/fileio.py"
# root_list = [root_dir2, root_dir1]
# # # print(pyan.create_callgraph(filenames=root_list))
# # # HTML(pyan.create_callgraph(filenames=root_list, format="html"))
# #
# res = pyan.create_callgraph(root_list, format="dot")
# # # # with open("test.dot","w") as f:
# # # #     f.write(res)
# # print(eval(res))
# # file = open('Source.gv', 'r')
# # js = file.read()
# # dic = json.loads(js)
# # print(dic)
# graph = graphviz.Source(res)
# graph.view()

# a = [1,2,3,4,5]
# print(a.pop(0))
# print(a)
# print(a[2:3])

import difflib
#
print(difflib.SequenceMatcher((lambda x: x == "_"), "savedir", "dirsave").ratio())

# for i in range(5):
#     if i > 2:
#         print(i,"asdf")
#     else:
#         print(i)
#         continue

# import graphviz
# import pyan
#
# root_dir1 = "/Users/liufan/program/PYTHON/SAP/PrivacyScan/systementrance.py"
# root_dir2 = "/Users/liufan/program/PYTHON/SAP/PrivacyScan/utils/fileio.py"
# root_list = [root_dir2, root_dir1]
#
# res = pyan.create_callgraph(root_list, format="dot")
#
# graph = graphviz.Source(res)
# graph.view()

# a = [(1, [2, 3, 4, 5])]
# b = [3, 4, 5]
# a.append((4, b))
#
# print(a)
