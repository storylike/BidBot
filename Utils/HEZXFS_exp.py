import os
import sys
import time
import re
import matplotlib.pyplot as plt
import datetime

sys.path.append('..')
from config import LSSC_DATEFORMAT

START_DATE = "2018-01-22"
END_DATE = "2018-06-22"

date_start = datetime.datetime.strptime(START_DATE, LSSC_DATEFORMAT)
date_end = datetime.datetime.strptime(END_DATE, LSSC_DATEFORMAT)
date_temp = date_start

temp_dict = {0: 0xc0, 1: 0xc0, 2: 0xc0, 3: 0xc0, 4: 0xc0, 5: 0xc0, 6: 0xc0, 7: 0xc0, 8: 0xc0, 9: 0xc0}

result_dict = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}


def clearresult():
    global result_dict
    for k, v in result_dict.items():
        result_dict[k] = 0


def CountNumAndSort(list_raw):
    """
    Count numbers from today's database and generate a sorted lenghao list.
    :param list_raw:
    :return:
    """
    global result_dict
    clearresult()
    for items in list_raw:
        for x in items:
            result_dict[x] = result_dict[x] + 1
    result = sorted(result_dict.items(), key=lambda d: d[1], reverse=False)
    return result


if __name__ == '__main__':
    earn_list = []
    # global date_start, date_end, result_dict
    while date_temp <= date_end:
        final = {"miss": 0, "hit": 0}
        with open("..\\Data\\" + date_temp.strftime("%Y-%m-%d") + '.txt', 'r') as record:
            line_list = []
            lenghao_last = []
            clearresult()
            print(result_dict)
            next_run = True

            for line in record.readlines():
                if line:
                    line_record = list(line.split('.')[1].strip())
                    line_list.append(line_record)

            if len(line_list) > 0:
                for index, item in enumerate(line_list, 0):
                    if index >= 24:
                        lenghao = CountNumAndSort(line_list[0:index])
                        lenghao_last.append(lenghao[-1][0])
                        lenghao_last.append(lenghao[-2][0])
                        if set(lenghao_last) & set([line_list[index][-1], line_list[index][-2]]):
                            final["hit"] = final["hit"] + 1
                            print("{0}:hit 热号:{1}".format(str(index+1), str(lenghao_last)))
                            # print("    miss")
                        else:
                            final["miss"] = final["miss"] + 1
                            print("{0}:miss 热号:{1}".format(str(index+1), str(lenghao_last)))
                            # print("    hit")
                    lenghao_last = []

            net_earn = 59 * final["hit"] - 36 * final["miss"]
            earn_list.append(net_earn)
            if net_earn < 0:
                '''
                print("================================================================================\
                ===========================================================================================")
                '''
            print("{0} {1} Earn: {2}".format(date_temp.strftime("%Y-%m-%d"), str(final), str(net_earn)))
            print(sorted(result_dict.items(), key=lambda d: d[1], reverse=False))
            final["miss"] = 0
            final["hit"] = 0
        date_temp = date_temp + datetime.timedelta(days=1)

    total_earn = 0
    for earn in earn_list:
        total_earn = total_earn + earn

    print("Total Earn: {0}".format(str(total_earn)))

    # earn_list.insert(0, -10)
    # earn_list.insert(0, -100)
    # earn_list.insert(0, -200)
    # earn_list.insert(0, -400)
    # earn_list.insert(0, -1000)

    time_line = list(range(len(earn_list)))

    plt.bar(time_line, earn_list, 0.5)
    # plt.set_xticks(range(len(ratio_list)))
    # plt.set_xticklabels(ratio_list)
    plt.show()
