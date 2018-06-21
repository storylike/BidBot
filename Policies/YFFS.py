import sys
import time
from .Base import BasePolicy
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.common.keys import Keys
sys.path.append('..')
from config import BID_UNIT_VALUE_MAP

class YFFS(BasePolicy):
    def __init__(self, driver):
        """
        Init method.
        """
        super().__init__(driver)
        self.name = 'BASE'
        self.driver = driver
        # Unit: FEN
        self.bidunit = BID_UNIT_VALUE_MAP["JIAO"]
        # OriginalTable
        #self.bidreferencetable = {0:0, 1:0, 2:0, 3:1, 4:2, 5:4, 6:8, 7:16, 8:32, 9:64, \
        #                     10:200, 11:400, 12:800, 13:1600, 14:3200, 15:6400, 16:12800, 17:25600, 18:10000, \
        #                     19:20000, 20:40000
        #                     }
        # Stop losses at 17
        self.bidreferencetable = {0: 0, 1: 0, 2: 0, 3: 1, 4: 2, 5: 4, 6: 8, 7: 16, 8: 32, 9: 64,
                                  10: 200, 11: 400, 12: 800, 13: 1600, 14: 3200, 15: 6400, 16: 12800, 17: 25600, 18: 0,
                                  19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0
                                  }
        self.current_bid_list = []
        # biddict: {bidnum:[NotRecentlyOccurredRounds, LastBidCount]}
        self.biddict = {0: [0xff, 0], 1: [0xff, 0], 2: [0xff, 0], 3: [0xff, 0], 4: [0xff, 0],
                        5: [0xff, 0], 6: [0xff, 0], 7: [0xff, 0], 8: [0xff, 0], 9: [0xff, 0]
                        }


    def CreateBidDict(self):
        """
        Fulfill NotRecentlyOccurredRounds fields in biddict.
        :return:
        """
        self.current_bid_list = self.datatoday
        self.logger("YFFS Policy: CreateBidDict start...")
        self.logger("YFFS Policy: today's data:")
        for items in self.current_bid_list:
            self.logger("        {0}".format(str(items)))
        for key,value in self.biddict.items():
            index = -1
            increment = 0
            found = True
            while str(key) not in self.datatoday[index-increment]:
                increment = increment + 1
                if increment >= 20 or increment + 1 > len(self.datatoday):
                    found = False
                    break
            if found is True:
                self.biddict[key][0] = increment

        self.logger("YFFS Policy: biddict:")
        for key,value in self.biddict.items():
            self.logger("       {}: {} {}".format(str(key), str(value[0]), str(value[1])))


    def UpdateBidDict(self):
        """
        When each new round starts, we will need to update biddict.
        :return:
        """
        self.logger("In UpdateBidDict")
        self.logger("datatoday[-1] = {}".format(str(self.datatoday[-1])))
        self.logger("Before BidDict Update:")
        self.logger("    BidDict: {}".format(str(self.biddict)))
        for key, value in self.biddict.items():
            if str(key) in set(self.datatoday[-1]):
                self.biddict[key][0] = 0
            else:
                self.biddict[key][0] = self.biddict[key][0] + 1
        self.logger("After BidDict Update:")
        self.logger("    BidDict: {}".format(str(self.biddict)))

    def GetHistoryData(self, driver):
        """
        This policy model need to get enough history data for analysis.
        :param driver:
        :return:
        """
        historydata = []
        soup = BeautifulSoup.BeautifulSoup()
        return historydata

    def UpdateHistoryData(self, driver):
        """
        When time pass by, this history data need to be updated as new data is generated
        :param self:
        :param driver:
        :return:
        """
        historydata = []
        return historydata

    def Predict(self, data):
        """
        Policy core functionality. In this method, latest history data is analyzed and candidate number list for next
        round is generated.
        :param self:
        :param data:
        :return:
        """
        predicted = self.biddict
        return predicted

    def WaitForBidStart(self):
        """
        Wait for biding cycle starts: skipping period 2:00 - 10:00 everyday.
        :param self:
        :return:
        """
        cur_time = time.strftime('%H:%M:%S')
        self.logger("WaitForBidStart...")
        while (cur_time > '02:00:00') and (cur_time < '10:00:00'):
            # I would only work after 10 AM :)
            self.logger("    Wait 60 seconds...")
            time.sleep(20)
            self.driver.find_element_by_css_selector("a[class='btn b0'][data-bettype='1'][data-subid='2345']").click()
            time.sleep(20)
            self.driver.find_element_by_css_selector("a[class='btn b0'][data-bettype='10'][data-subid='45']").click()
            time.sleep(20)

    def StartBid(self):
        """
        Start bidding.
        :param biddict:
        :return:
        """
        # First, we need to wait for bid cycle start.
        #self.WaitForBidStart()
        self.logger("Round:{} Policy: YFFS, StartBiding...". format(str(self.round)))
        self.logger(str(self.biddict))

        # set sleeping interval
        sleeping = 40
        cur_time = time.strftime('%H:%M:%S')
        if (cur_time >= '10:00:00') and (cur_time < '22:00:00'):
            sleeping = 60

        time.sleep(sleeping)
        for key, value in self.biddict.items():
            if (value[0] < 20) and (value[0] != 0xff) and (value[0] in self.bidreferencetable) and (self.bidreferencetable[value[0]] > 0):
                # Click WuXing
                time.sleep(3)
                self.driver.find_element_by_css_selector("a[class='btn b0'][data-bettype='1'][data-subid='12345']").click()
                time.sleep(2)
                # Click BuDingWei
                self.driver.find_element_by_css_selector("a[class='btn b0'][data-bettype='5'][data-subid='1123']").click()
                time.sleep(2)
                # WuXingYiMa BuDingWei
                self.driver.find_element_by_css_selector("input[name='r0'][type='radio'][class='pointer'][value='2_5_112345']").click()
                time.sleep(2)
                # Select Bid Number, 5, e.g.
                # driver.find_element_by_css_selector("a[data-num='5'][class='isNum']").click()
                # We should apply actual bid num from biddict:
                self.driver.find_element_by_css_selector("a[data-num={0}][class='isNum']".format( \
                    ''.join(["\'", str(key), "\'"]))).click()
                time.sleep(1)
                # Drag slider bar to leftmost to get most bonus rate
                dragsource = self.driver.find_element_by_css_selector(
                    "span[class='ui-slider-handle ui-state-default ui-corner-all'][tabindex='0']")
                dragtarget = self.driver.find_element_by_css_selector("i[class='fa fa-plus-circle fs18 minus']")
                ActionChains(self.driver).drag_and_drop(dragsource, dragtarget).perform()
                time.sleep(1)
                # Set Bid value according to biddict[key][1]
                self.driver.find_element_by_id('buyamount').clear()
                time.sleep(1)
                self.driver.find_element_by_id('buyamount').send_keys(str(self.bidreferencetable[self.biddict[key][0]]))
                time.sleep(1)
                # Select bid unit
                # value = 1 : yuan
                # value = 10 : jiao
                # value = 100 : fen
                select = Select(self.driver.find_element_by_id("selectdollarunit"))
                select.select_by_value(str(self.bidunit))
                time.sleep(1)
                # Add to bid list
                self.driver.find_element_by_css_selector("a[class='btn2'][id='seleall']").click()
                time.sleep(1)
                # Confirm bid
                self.driver.find_element_by_css_selector("a[class='btn b3'][id='gamebuy']").click()
                time.sleep(3)
                # Handle pop ups after bid confirmation
                # Get last popped up dialog box, that's a bid order confirmation
                confirm_box = self.driver.find_elements_by_css_selector("button[type='button'][i-id='ok'][class='fix-ui-dialog-autofocus']")[-1]
                time.sleep(1)
                confirm_box.click()
                time.sleep(3)
                # At last, we should update biddict[key][1] to the actual value we are placing a bid
                self.biddict[key][1] = self.bidreferencetable[self.biddict[key][0]]
                self.logger("Biding done with num:{0}, amount:{1}".format(str(key), str(self.biddict[key][1])))
                time.sleep(1)
        self.logger("Round:{} Policy:YFFS End bidding...".format(str(self.round)))


    def EndBid(self):
        """
        End biding, clean up.
        :return:
        """
        self.logger("Round {round} end, policy:{name}, bid number(s): {numlist}".format(
            round=self.round,
            name=self.name,
            numlist=str(self.current_bid_list)
            ))

    def GotoBidPage(self):
        """
        Goto Bid page.
        :return:
        """
        # Click SSC link tag in main page
        #self.driver.find_elements_by_class_name('product_01')[0].click()
        #time.sleep(5)
        # Cancel POPUP after SSC Link click
        if self.driver.find_elements_by_class_name('dont-popup')[0].is_displayed():
            self.driver.find_elements_by_class_name('dont-popup')[0].click()
            self.driver.find_elements_by_class_name('fa-close')[0].click()