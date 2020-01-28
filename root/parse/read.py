"""

数据库读取类
给文本处理、特征处理分配一定的权重
返回推荐top8

"""

from sqlalchemy import create_engine
import pymysql
from root.parse.config import *
from numpy import *
from root.parse.service.text import *
from root.parse.service.fs import *


def text_pre_process(title):

    return title.strip().strip('大会').strip('会议').strip('峰会').strip('会').strip('年会')


def address_prr_process(address):

    return address.strip().strip('中国')


class Meeting:

    def __init__(self, mid, title, address, fs):

        self.mid = mid
        self.title = title
        self.address = address
        self.fs = fs


class Reader:

    def __init__(self, table):

        self.table = table
        self.db = pymysql.connect(**config)
        self.cursor = self.db.cursor()
        create_engine(engine_config)
        self.all_meetings = self.get_all_meetings()

    def get_all_meetings(self):

        sql = "select mid, title, address, f1, f2, f3 from {}".format(self.table)
        self.cursor.execute(sql)
        rst = self.cursor.fetchall()
        all_mat = mat(array(rst))
        all_mat[all_mat == None] = -1
        all_mat[:, 3:6] = all_mat[:, 3:6].astype(int)
        for sin in all_mat:
            sin[0, 1] = text_pre_process(sin[0, 1])
            sin[0, 2] = address_prr_process(sin[0, 2])

        # meetings = []
        # for meeting in all_mat:
        #     m = Meeting(meeting[0, 0], meeting[0, 1], meeting[0, 2], meeting[0, 3: 6])
        #     meetings.append(m)

        return all_mat

    def get_meeting(self, mid):

        sql = "select mid, title, address, f1, f2, f3 from {} where mid = {}".format(self.table, mid)
        self.cursor.execute(sql)
        rst = self.cursor.fetchall()[0]
        # fs = []
        #
        # for i in range(3, 6):
        #     fs.append(-1 if not rst[i] else int(rst[i]))
        # m = Meeting(rst[0], rst[1], rst[2], [int(element) for element in fs])
        return rst

    def get_meeting_list(self, mid_list):

        format_rst = '('
        format_content = [str(mid) + ', ' for mid in mid_list[:-1]]
        format_content += str(mid_list[-1])
        for s in format_content:
            format_rst += s
        format_rst += ')'
        sql = "select mid, title, address, f1, f2, f3 from {} where mid in {}".format(self.table, format_rst)
        self.cursor.execute(sql)
        rst = self.cursor.fetchall()
        rst_mat = mat(array(rst))
        rst_mat[rst_mat == None] = -1

        rst_mat[:, 0] = rst_mat[:, 0].astype(int)
        rst_mat[:, 3:6] = rst_mat[:, 3:6].astype(int)

        return rst_mat

    @staticmethod
    def pre_process(data):
        pass


if __name__ == '__main__':

    reader = Reader('meeting')
    meetings = reader.all_meetings
    text = meetings[:, 0:3]
    fs = meetings[:, [0, 3, 4, 5, ]]

    history = reader.get_meeting_list([6, 7, ])

    text_rate = do_text(history[:, :3], text)
    fs_rate = do_fs(history[:, [0, 3, 4, 5]], fs)
    rst = []

    for i in range(6):
        if not text_rate[i] in rst:
            rst.append(int(text_rate[i]))
        if not fs_rate[i] in rst:
            rst.append(int(fs_rate[i]))



