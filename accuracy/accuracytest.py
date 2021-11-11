import xlrd


def load_location(file_path):
    wk_bk = xlrd.open_workbook(file_path)
    wk_all = wk_bk.sheet_by_index(0)

    location_list = [(location.split('/')[0].replace('.py', '').replace('.', '/') + '.py', int(location.split('/')[1]))
                     for location in list(wk_all.col_values(0))[2:] if location != '']

    datatype_list = [data_type.split('/')[-1] for data_type in wk_all.col_values(1)[2:] if data_type != '']

    purpose_list = [purpose for purpose in wk_all.col_values(2)[2:] if purpose != '']

    location_dict = {}
    for i in range(len(location_list)):
        if location_list[i] in location_dict.keys():
            location_dict[location_list[i]].append((datatype_list[i], purpose_list[i]))
        else:
            location_dict[location_list[i]] = [(datatype_list[i], purpose_list[i])]

    print(len(location_dict.items()))
    for item, value in location_dict.items():
        print(item, value)

    return location_dict


def test_recall(suspected_node_list, source):
    """
    查全率=（检索出的相关信息量/系统中的相关信息总量）
    :param suspected_node_list:
    :param source:
    :return:
    """
    location_dict = load_location("../项目校对表.xlsx")
    location_num = len(location_dict.keys())
    recall_location = 0
    recall_accurate = 0
    for node in suspected_node_list:
        if (node.file_path.replace(source + '/', ''), node.line_no) in location_dict.keys():
            print()
            recall_location += 1
            # if node.
    pass


def test_accuracy():
    pass


if __name__ == '__main__':
    load_location("../项目校对表.xlsx")
