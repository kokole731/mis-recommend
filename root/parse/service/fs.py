"""
会议特征处理
input(列表):用户历史
output(列表):特征处理结果矩阵（所有会议）
"""

from numpy import *


def do_fs(hist, meeting_fs):

    hist = hist.astype(int)
    meeting_fs = meeting_fs.astype(int)
    rate_mat = zeros((len(meeting_fs), 1))
    rate_mat = hstack((meeting_fs, rate_mat))

    for his in hist:

        for sin in rate_mat:

            if not his[0, 0] == sin[0, 0]:
                a, b = list(), list()
                for i in range(1, 4):
                    a.append(sin[0, i])
                    b.append(his[0, i])

                both = [x for x in a if x in b]
                while -1 in both:
                    both.remove(-1)
                sin[0, -1] += len(both)
    rate_mat[:, -1] = rate_mat[:, -1] / len(hist) / 3

    rst = rate_mat[:, [0, 4]]
    rst_dict = dict()
    for r in rst:
        rst_dict[r[0, 0]] = r[0, 1]
    # sorted(rst_dict.items(), key=lambda item: item[1], reverse=True)
    f = zip(rst_dict.values(), rst_dict.keys())
    r = sorted(f)[-6:]
    top6 = []
    for element in r:
        top6.append(int(element[1]))

    return top6[::-1]

