import os
import sys
import time
import re
import urllib
import urllib.request
from bs4 import BeautifulSoup
import datetime

sys.path.append('..')
from config import LSSC_URL,LSSC_DATEFORMAT

START_DATE = "2018-06-22"
END_DATE = "2018-06-22"
print(LSSC_URL)
print(LSSC_DATEFORMAT)
date_start = datetime.datetime.strptime(START_DATE, LSSC_DATEFORMAT)
date_end = datetime.datetime.strptime(END_DATE, LSSC_DATEFORMAT)
date_temp = date_start

while date_temp <= date_end:
    date_time = date_temp.strftime("%Y-%m-%d")
    URL = ''.join([LSSC_URL, date_time, '_', date_time])
    #print (date_time)
    page = urllib.request.urlopen(URL)

    soup = BeautifulSoup(page.read(),'html.parser')

    tablelist = soup.findAll("td", attrs={"class":"red big"})
    result = []
    for i,l in enumerate(tablelist):
        pattern = re.compile(r'\d+')
        result_item = pattern.findall(str(l))
        record = "{0} {1}.{2}".format(date_time, str(i+1), str(result_item[0]))
        #print (record)
        result.append(record)
    with open("..\\Data\\" + date_time + ".txt", 'w+') as filedata:
        for x in result:
            filedata.write(x)
            filedata.write('\n')
    page.close()
    date_temp = date_temp + datetime.timedelta(days=1)
    time.sleep(1)
