import time
import re
import urllib
import urllib.request
from bs4 import BeautifulSoup
import datetime
import sys
sys.path.append('..')
from config import LSSC_URL, LSSC_DATEFORMAT, DATETIMEFMT
from urllib.error import URLError


class BasePolicy(object):
    """
    This is policy base class, all practical policies need to be inherited from this base class.
    """
    def __init__(self, driver):
        self.name = 'BASE'
        self.updated = False
        self.round = 0xff
        self.driver = driver
        self.current_bid_list = []
        self.datatoday = []
        self.lenghao_sorted = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    def CrawlAndBuildDataTable(self):
        """
        This method crawls desired page, then build and store data we desire.
        :return:
        """
        retries = 3
        self.logger("Start Crawling today's LSSC data...")
        date_today = datetime.datetime.now().strftime(LSSC_DATEFORMAT)
        URL = ''.join([LSSC_URL, date_today, '_', date_today])
        for i in range(retries):
            try:
                self.logger("Start to open URL, retries = {}".format(str(i)))
                page = urllib.request.urlopen(URL, timeout=40)
                break
            except URLError:
                self.logger("Failed to open URL, retries = {}".format(str(i)))
            time.sleep(15)
        content = page.read()
        soup = BeautifulSoup(content, 'html.parser')
        tablelist = soup.findAll("td", attrs={"class":"red big"})
        result = []
        for l in tablelist:
            pattern = re.compile(r'\d+')
            result_item = pattern.findall(str(l))
            result.append(list(str(result_item[0])))
        for index,items in enumerate(result):
            self.logger("      {:0>3}.  {}".format(str(index+1), items))
        page.close()
        return result

    def GetTodayData(self):
        """
        This policy model need to get enough today's data for analysis.
        :return:
        """
        self.datatoday = self.CrawlAndBuildDataTable()

    def UpdateTodayData(self):
        """
        When time pass by, today's data need to be updated as new data is generated
        :param self:
        :return:
        """
        # Set sleeping interval
        cur_time = time.strftime('%H:%M:%S')
        sleeping = 30
        if (cur_time >= '10:00:00') and (cur_time < '22:00:00'):
            sleeping = 60
        self.logger("Trying to update today's data...")
        temp_data = self.CrawlAndBuildDataTable()
        while len(temp_data) == len(self.datatoday):
            self.logger("Data identical to previous fetched, sleep {} seconds and retry.".format(sleeping))
            time.sleep(sleeping)
            temp_data = self.CrawlAndBuildDataTable()
        assert len(temp_data) == len(self.datatoday) + 1, "Unexpected data length captured!"
        self.logger("New data record found: {}. Start updating data.".format(str(temp_data[-1])))
        #for index, items in enumerate(temp_data):
        #    assert self.datatoday[index] == items, \
        #        "datatoday[{0}]={1}, temp_data[{0}]={2}".format(str(index), str(self.datatoday[index]), str(items))
        self.datatoday = temp_data
        self.round = len(self.datatoday)
        for index,items in enumerate(self.datatoday):
            self.logger("In UpdateTodayData, Datatoday:")
            self.logger("      {:0>3}.  {}".format(str(index+1), items))
        self.lenghao_sorted = self.CountNumAndSort(self.datatoday)
        self.updated = True

    def CountNumAndSort(self, list_raw):
        """
        Count numbers from today's database and generate a sorted lenghao list.
        :param self:
        :param list_raw:
        :return:
        """
        result_temp = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        self.logger("CountNumAndSort Start...")
        for items in list_raw:
            for x in items:
                result_temp[int(x)] = result_temp[int(x)] + 1
        result = sorted(result_temp.items(), key=lambda d:d[1], reverse = False)
        self.logger("Generated lenghao list: {0}".format(result))
        return result

    def Predict(self):
        """
        Policy core functionality. In this method, latest history data is analyzed and candidate number list for next
        round is generated.
        :return:
        """
        predicted = {}
        return predicted

    def StartBid(self, bidlist=[]):
        pass

    def EndBid(self):
        self.logger("Round {round} end, policy:{name}, bid number(s): {numlist}".format(
            round=self.round,
            name=self.name,
            numlist=str(self.current_bid_list)
            ))

    def WaitForBidStart(self):
        """
        Wait for biding cycle starts: skipping period 2:00 - 10:00 everyday.
        :param self:
        :return:
        """
        cur_time = time.strftime('%H:%M:%S')
        while (cur_time > '02:00:00') and (cur_time < '10:00:00'):
            # I'm only focusing on time period of 10:00 - 22.00 every day, with drawing lottery interval being 10 minutes.
            time.sleep(30)

#    def GotoBidPage(self):
#        pass

    def logger(self, logmsg):
        """
        Logger method.
        :param self:
        :param logmsg:
        :return:
        """
        date_today = time.strftime('%Y-%m-%d')
        log_time = time.strftime(DATETIMEFMT)
        with open('Log\\log_' + date_today + '.txt', 'a+') as log:
            log.write(' '.join([log_time, logmsg, '\n']))
        print(' '.join([log_time, logmsg,'\n']))
