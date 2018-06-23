import sys
import time
from .Base import BasePolicy
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
sys.path.append('..')

class WXYMBDW(BasePolicy):
    def __init__(self, driver):
        """
        Init method.
        """
        super().__init__(driver)
        self.name = 'YFFS'
        self.driver = driver
        # Unit: YUAN
        self.bid_unit = 1
        self.bid_amount = 1

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
        self.logger("Round:{} Policy: WXYMBDW, StartBiding...". format(str(self.round)))
        self.logger(str(self.rehao_sorted))

        # set sleeping interval
        sleeping = 20
        cur_time = time.strftime('%H:%M:%S')
        if (cur_time >= '10:00:00') and (cur_time < '22:00:00'):
            sleeping = 60
        time.sleep(sleeping)

        bid_candidate = []
        bid_candidate.append(self.rehao_sorted[0][0])
        bid_candidate.append(self.rehao_sorted[1][0])
        if int(self.rehao_sorted[0][1]) >= 3:
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
            # We should apply actual bid num from bid_candidate:
            for key in bid_candidate:
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
            self.driver.find_element_by_id('buyamount').send_keys(str(self.bid_amount))
            time.sleep(1)
            # Select bid unit
            # value = 1 : yuan
            # value = 10 : jiao
            # value = 100 : fen
            select = Select(self.driver.find_element_by_id("selectdollarunit"))
            select.select_by_value(str(self.bid_unit))
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
            self.logger("Biding done with num:{0}, amount:{1}".format(bid_candidate, str(self.bid_amount)))
            time.sleep(1)
        self.logger("Round:{} Policy:WXYMBDW End bidding...".format(str(self.round)))


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