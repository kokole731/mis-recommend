from root.parse.read import *
from numpy import *
from root.parse.service.text import *
from root.parse.service.fs import *


class Parse:

    def __init__(self, mid_list, ):

        self.mid_list = mid_list

    def get_result(self):

        reader = Reader('meeting')
        meetings = reader.all_meetings
        text = meetings[:, 0:3]
        fs = meetings[:, [0, 3, 4, 5, ]]

        history = reader.get_meeting_list(self.mid_list)

        text_rate = do_text(history[:, :3], text)
        fs_rate = do_fs(history[:, [0, 3, 4, 5]], fs)
        rst = []

        for i in range(6):
            if not text_rate[i] in rst:
                rst.append(text_rate[i])
            if not fs_rate[i] in rst:

                rst.append(fs_rate[i])

        return rst


if __name__ == '__main__':

    parse = Parse([6, 7])
    print(parse.get_result())
