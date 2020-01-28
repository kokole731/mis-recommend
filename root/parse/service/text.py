"""
会议标题、举办地点处理
input(列表):用户的历史会议
output(列表):文本处理结果矩阵，（所有会议）
"""

from numpy import *
import difflib


# 函数
def do_text(hist, meeting_text):

    title_list = [0] * len(meeting_text)
    address_list = [0] * len(meeting_text)

    # for meeting in hist:

    for hit in hist:
        id = 0
        for sin in meeting_text:

            simi1 = difflib.SequenceMatcher(None, hit[0, 1], sin[0, 1]).quick_ratio()
            title_list[id] += simi1 if simi1 != 1 else 0
            # sin[0, -2] += simi1 if simi1 != 1 else 0

            simi2 = difflib.SequenceMatcher(None, hit[0, 2], sin[0, 2]).quick_ratio()
            address_list[id] += simi2
            # sin[0, -1] += simi2

    title_list = [element/len(hist) for element in title_list]
    address_list = [element/len(hist) for element in address_list]

    rst = []
    for i in range(len(title_list)):
        rst.append(title_list[i] + address_list[i])

    # rate_mat[:, -2:] = rate_mat[:, -2:] / len(hist)
    # rate_mat[:, -3] = rate_mat[:, -2] + rate_mat[:, -1]

    # rst = rate_mat[:, [0, 3]]

    rst_dict = dict()

    for i in range(len(rst)):
        rst_dict[meeting_text[i, 0]] = rst[i]

    # for r in rst:
    #     rst_dict[r[0, 0]] = r[0, 1]
    # sorted(rst_dict.items(), key=lambda item: item[1], reverse=True)
    f = zip(rst_dict.values(), rst_dict.keys())
    r = sorted(f)[-6:]
    top6 = []
    for element in r:
        top6.append(int(element[1]))

    return top6[::-1]





