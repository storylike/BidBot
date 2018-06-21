import sys
import time
from .Base import BasePolicy
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.common.keys import Keys
sys.path.append('..')
from config import BID_UNIT_VALUE_MAP

class HEZXFS(BasePolicy):
    def __init__(self, driver):
        """
        Init method.
        """
        super().__init__(driver)
        self.name = 'HEZXFS'
        self.driver = driver
        # Unit: FEN
        self.bidunit = BID_UNIT_VALUE_MAP["JIAO"]
        self.bidamount = 1
        self.hot_numbers = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}

    def ReadyForBid(self):
        """
        Wait for biding cycle starts: skipping period 2:00 - 10:00 everyday.
        :param self:
        :return:
        """
        ready = True
        cur_time = time.strftime('%H:%M:%S')
        if '00:00:00' <= cur_time <= '02:00:00':
            ready = False
        return ready


    def StartBid(self):
        """
        Start bidding.
        :param biddict:
        :return:
        """
        # First, we need to wait for bid cycle start.
        if not self.ReadyForBid():
            return
        self.logger("Round:{} Policy: HEZXFS, StartBiding...". format(str(self.round)))
        self.logger(str(self.lenghao_sorted))

        # set sleeping interval
        sleeping = 40
        cur_time = time.strftime('%H:%M:%S')
        if (cur_time >= '10:00:00') and (cur_time < '22:00:00'):
            sleeping = 60
        time.sleep(sleeping)

        # Click WuXing
        time.sleep(3)
        self.driver.find_element_by_css_selector("a[class='btn b0'][data-bettype='1'][data-subid='12345']").click()
        time.sleep(2)
        # Click ErXing
        self.driver.find_element_by_css_selector("a[class='btn b0'][data-bettype='1'][data-subid='12']").click()
        time.sleep(2)
        # Click HEZXFS
        self.driver.find_element_by_css_selector("input[name='r0'][type='radio'][class='pointer'][value='2_1_45']").click()
        time.sleep(2)

        # Select Bid Number, 5, e.g.
        # driver.find_element_by_css_selector("a[data-num='5'][class='isNum']").click()
        # exclude bid two numbers directly from lenghao_sorted[0][0] and lenghao_sorted[1][0]:
        for x in set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) - set([int(self.lenghao_sorted[0][0]), int(self.lenghao_sorted[1][0])]):
            print("    Trying to select: {0}".format(str(x)))
            need_select = self.driver.find_elements_by_css_selector("a[href='javascript:;'][data-num={0}]".format(
                ''.join(["\'", str(x), "\'"])))
            print(need_select)
            for items in need_select:
                items.click()
                time.sleep(1)
            need_select = []
        # Drag slider bar to leftmost to get most bonus rate
        dragsource = self.driver.find_element_by_css_selector(
            "span[class='ui-slider-handle ui-state-default ui-corner-all'][tabindex='0']")
        dragtarget = self.driver.find_element_by_css_selector("i[class='fa fa-plus-circle fs18 minus']")
        ActionChains(self.driver).drag_and_drop(dragsource, dragtarget).perform()
        time.sleep(1)
        # Set Bid value according to biddict[key][1]
        self.driver.find_element_by_id('buyamount').clear()
        time.sleep(1)
        self.driver.find_element_by_id('buyamount').send_keys(str(self.bidamount))
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
        # At last, log this bid
        self.logger("Biding done with num:{0},{1}, amount:{1}".format(str(self.lenghao_sorted[0][0]),
                                                                      str(self.lenghao_sorted[1][0]),
                                                                      str(self.bidamount)
                                                                      )
                    )
        time.sleep(1)

        self.logger("Round:{} Policy: HEZXFS End bidding...".format(str(self.round)))


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