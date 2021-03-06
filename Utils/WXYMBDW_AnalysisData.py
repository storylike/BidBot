import os
import sys
import time
import re
import matplotlib.pyplot as plt
import datetime

sys.path.append('..')
from config import LSSC_DATEFORMAT

START_DATE = "2018-04-22"
END_DATE = "2018-06-22"

date_start = datetime.datetime.strptime(START_DATE, LSSC_DATEFORMAT)
date_end = datetime.datetime.strptime(END_DATE, LSSC_DATEFORMAT)
date_temp = date_start

temp_dict = {0: 0xc0, 1: 0xc0, 2: 0xc0, 3: 0xc0, 4: 0xc0, 5: 0xc0, 6: 0xc0, 7: 0xc0, 8: 0xc0, 9: 0xc0}

result_dict = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}

rehao_sorted = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}


def clearresult():
    global result_dict
    for k, v in result_dict.items():
        result_dict[k] = 0
    for k, v in rehao_sorted.items():
        rehao_sorted[k] = 0


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

def CountRehaoAndSort(list_raw):
    """
    Count numbers from today's database and generate a sorted lenghao list.
    :param list_raw:
    :return:
    """
    global rehao_sorted
    for k, v in rehao_sorted.items():
        rehao_sorted[k] = 0
    for items in list_raw:
        for k, v in rehao_sorted.items():
            if k in items:
                rehao_sorted[k] = rehao_sorted[k] + 1
            else:
                rehao_sorted[k] = 0
    result = sorted(rehao_sorted.items(), key=lambda d: d[1], reverse=True)
    return result


if __name__ == '__main__':
    earn_list = []
    # global date_start, date_end, result_dict
    while date_temp <= date_end:
        final = {"miss": 0, "hit": 0,  "half_hit": 0}
        with open("..\\Data\\" + date_temp.strftime("%Y-%m-%d") + '.txt', 'r') as record:
            line_list = []
            lenghao_last = []
            rehao_list = []
            clearresult()
            print(result_dict)
            bid_run = False

            for line in record.readlines():
                if line:
                    line_record = list(line.split('.')[1].strip())
                    line_list.append(line_record)

            if len(line_list) > 0:
                for index, item in enumerate(line_list, 0):
                    bid_run = False
                    if index >= 24:
                        lenghao = CountNumAndSort(line_list[0:index])
                        lenghao_last.append(lenghao[-1][0])
                        lenghao_last.append(lenghao[-2][0])

                        rehao = CountRehaoAndSort(line_list[0:index])
                        rehao_list.append(rehao[0][0])
                        #rehao_list.append(rehao[1][0])
                        if int(rehao[1][1]) >= 3:
                            if len(set(rehao_list) & set(line_list[index])) == 2:
                                final["hit"] = final["hit"] + 1
                                print("{0}:hit 热号:{1}, 开:{2}".format(str(index+1), str(rehao[0][0]+':'+str(rehao[0][1])+'次'), line_list[index]))
                                # print("    miss")
                            elif len(set(rehao_list) & set(line_list[index])) == 1:
                                final["half_hit"] = final["half_hit"] + 1
                                print("{0}:half_hit 热号:{1}, 开:{2}".format(str(index+1), str(rehao[0][0]+':'+str(rehao[0][1])+'次'), line_list[index]))
                                # print("    hit")
                            else:
                                final["miss"] = final["miss"] + 1
                                print("{0}:miss 热号:{1}, 开:{2}".format(str(index+1), str(rehao[0][0]+':'+str(rehao[0][1])+'次'), line_list[index]))
                    lenghao_last = []
                    rehao_list = []

            net_earn = 2.638 * final["hit"] + 0.319 * final["half_hit"] - 2 * final["miss"]
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
