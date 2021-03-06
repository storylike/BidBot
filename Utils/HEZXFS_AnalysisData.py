import os
import sys
import time
import re
import matplotlib.pyplot as plt  
import datetime
sys.path.append('..')
from config import LSSC_DATEFORMAT


START_DATE = "2009-12-13"
END_DATE = "2018-06-16"

date_start = datetime.datetime.strptime(START_DATE, LSSC_DATEFORMAT)
date_end = datetime.datetime.strptime(END_DATE, LSSC_DATEFORMAT)
date_temp = date_start

analysis_result = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0,
                   10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0,
                   21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0
                   }
temp_dict = {0: 0xc0, 1: 0xc0, 2: 0xc0, 3: 0xc0, 4: 0xc0, 5: 0xc0, 6: 0xc0, 7: 0xc0, 8: 0xc0, 9: 0xc0}

'''
def concatenate_all_history():
	"""

    :return:
    """
    file_list = []
    global date_end, date_temp
    while date_temp <= date_end:
        file_list.append("..\\Data\\" + date_temp.strftime("%Y-%m-%d") + ".txt")
        date_temp = date_temp + datetime.timedelta(days=1)
    print(file_list)
    with open("..\\Data\\temp.txt", "w") as temp:
        for txtfile in file_list:
            for txt in open(txtfile, 'r'):
                temp.write(txt)
'''
'''
            numbers = line.split('.')[1].strip()
            for k,v in temp_dict.items():
                if (str(k) in set(list(numbers))) and (v in analysis_result.keys()):
                    if temp_dict[k] >= 18:
                        print(' '.join([line.split(' ')[0], "号码:", str(k), "   ", str(temp_dict[k]), "次不中", "    期号.最终开出号码", line.split(' ')[1]]))
                    temp_dict[k] = 0
                    #print(temp_dict)
                    analysis_result[v] = analysis_result[v] + 1
                elif temp_dict[k] is 0xc0:
                    temp_dict[k] = 0
                else:
                    temp_dict[k] = temp_dict[k] + 1
                    #print(temp_dict)
'''

if __name__ == '__main__':
    #concatenate_all_history()
    for k,v in temp_dict.items():
        temp_dict[k] = 0xc0
    #print(temp_dict)
    '''
    while line:
        dates = line.split(' ')[0]
        rounds = line.split(' ')[1].split('.')[0]
        numbers = line.split('.')[1].strip()
        list_num = list(numbers)
        inc = 0
        # print(list_num)
        # print(list_all[-1-inc][-1])
        # print(list_all[-1-inc][-2])
        # print([list_all[-1-inc][-1], list_all[-1-inc][-2]])
        while (
                (inc < len(list_all)) and
                len(set([list_num[0], list_num[1]]) & set([list_all[-1 - inc][0], list_all[-1 - inc][1]]))
        ):
            inc = inc + 1

        list_all.append(list_num)
        analysis_result[inc] = analysis_result[inc] + 1
        if inc >= 8:
            print(' '.join([line.split(' ')[0], "号码:", str(list_num[-1]) + str(list_num[-2]), "    ", str(inc), "次不中", \
                            "      期号", line.split(' ')[1].split('.')[0], "    最终开出号码", numbers]))
        line = filedata.readline()
    '''
    with open("..\\Data\\temp.txt", 'r') as filedata:
        line = filedata.readline()
        list_all = []
        #print(line)
        while line:
            list_num = []
            dates = line.split(' ')[0]
            rounds = line.split(' ')[1].split('.')[0]
            numbers = line.split('.')[1].strip()
            list_num.append('.'.join([dates, rounds]))
            list_num.append(list(numbers))
            list_all.append(list_num)
            line = filedata.readline()

    for index, record in enumerate(list_all):
        inc = 0
        while (
                (index + 1 + inc < len(list_all)) and
                len(set([record[1][-1], record[1][-2]]) & set([list_all[index + 1 + inc][1][-1], list_all[index + 1 + inc][1][-2]]))
        ):
            inc = inc + 1
        analysis_result[inc] = analysis_result[inc] + 1
        if inc >= 8:
            print(' '.join([record[0].split('.')[0], "号码:", str(record[1][-1])+str(record[1][-2]), "    ", str(inc), "次不中", \
                                "      期号", record[0].split('.')[1], "    初始号码", str(record[1])]))


    total = 0
    for k,v in analysis_result.items():
        total = total + v

    print('total = {}'.format(total))
    print(analysis_result)
    calculated_list = [value for value in analysis_result.values()]
    ratio_list = ['%.2f' % (100*value/total) for value in calculated_list]

    x = list(range(len(calculated_list)))
    for i in range(len(x)):
        x[i] = x[i] + 1

    #fig,ax = plt.subplots()
    plt.bar(ratio_list, calculated_list, 0.5)
    #plt.set_xticks(range(len(ratio_list)))
    #plt.set_xticklabels(ratio_list)
    plt.show()