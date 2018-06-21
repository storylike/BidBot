import os
import sys
import time
import re
import matplotlib.pyplot as plt
import datetime
sys.path.append('..')
from config import LSSC_DATEFORMAT


START_DATE = "2017-12-16"
END_DATE = "2018-06-16"

date_start = datetime.datetime.strptime(START_DATE, LSSC_DATEFORMAT)
date_end = datetime.datetime.strptime(END_DATE, LSSC_DATEFORMAT)
date_temp = date_start


temp_dict = {0: 0xc0, 1: 0xc0, 2: 0xc0, 3: 0xc0, 4: 0xc0, 5: 0xc0, 6: 0xc0, 7: 0xc0, 8: 0xc0, 9: 0xc0}


result_dict = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}


def clearresult():
    global result_dict
    for k,v in result_dict.items():
        result_dict[k] = 0

def CountNumAndSort(list_raw):
    """
    Count numbers from today's database and generate a sorted lenghao list.
    :param list_raw:
    :return:
    """
    global result_dict
    for x in list_raw:
        result_dict[x] = result_dict[x] + 1
    result = sorted(result_dict.items(), key=lambda d: d[1], reverse=False)
    return result


if __name__ == '__main__':
    earn_list = []
    #global date_start, date_end, result_dict
    while date_temp <= date_end:
        final = {"miss": 0, "hit": 0}
        with open("..\\Data\\" + date_temp.strftime("%Y-%m-%d") + '.txt', 'r') as record:
            line = record.readline().strip()
            clearresult()
            lenghao_last = []
            line_list = []
            while line:
                #print(line)
                #print(line_list)
                #print(list(line.split('.')[1].strip()))
                line_record = list(line.split('.')[1].strip())
                line_list.append(line_record)
                #print(line_list)
                #print("第{}期：".format(line.split(' ')[1].split('.')[0]))
                lenghao = CountNumAndSort(line_record)
                #print("    冷号：" + str(lenghao))
                #print("    开出: {}".format(line.split('.')[1].strip()))
                if int(line.split(' ')[1].split('.')[0]) > 24:
                    if set(lenghao_last) & set([list(line)[-1], list(line)[-2]]):
                        final["miss"] = final["miss"] + 1
                        #print("    miss")
                    else:
                        final["hit"] = final["hit"] + 1
                        #print("    hit")
                    lenghao_last = []
                    lenghao_last.append(lenghao[0][0])
                    lenghao_last.append(lenghao[0][1])

                line = record.readline().strip()
            earn_list.append(31 * final["hit"] - 64 * final["miss"])
            print("{0} {1}".format(date_temp.strftime("%Y-%m-%d"), str(final)))
            final["miss"] = 0
            final["hit"] = 0
        date_temp = date_temp + datetime.timedelta(days=1)

    time_line = list(range(len(earn_list)))
    plt.bar(time_line, earn_list, 0.5)
    #plt.set_xticks(range(len(ratio_list)))
    #plt.set_xticklabels(ratio_list)
    plt.show()
