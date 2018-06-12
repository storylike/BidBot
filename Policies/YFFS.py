from Base import BasePolicy
import beautifulsoup


class YFFS(BasePolicy):
    def __init__(self):
        """
        Init method.
        """
        self.name = 'BASE'
        self.current_bid_list = []
        # biddict: {bidnum:[NotRecentlyOccurredRounds, LastBidCount]}
        self.biddict = {"0":[0,0], "1":[0,0], "2":[0,0], "3":[0,0], "4":[0,0], \
                        "5":[0,0], "6":[0,0], "7":[0,0], "8":[0,0], "9":[0,0] \
                        }
        pass
    def GetHistoryData(self, driver):
        """
        This policy model need to get enough history data for analysis.
        :param driver:
        :return:
        """
        soup = BeautifulSoup.BeautifulSoup()
        return historydata
    def UpdateHistoryData(self, driver):
        """
        When time pass by, this history data need to be updated as new data is generated
        :param self:
        :param driver:
        :return:
        """
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
    def StartBid(self, predicted):
        """
        :param self:
        :param bidlist:
        :return:
        """
        # Click BuDingWei
        driver.find_element_by_css_selector("a[class='btn b0'][data-bettype='5'][data-subid='1123']").click()

        # WuXingYiMa BuDingWei
        driver.find_element_by_css_selector(
            "input[name='r0'][type='radio'][class='pointer'][value='2_5_112345']").click()
        # Select Bid Number, 5, e.g.
        driver.find_element_by_css_selector("a[data-num='5'][class='isNum']").click()
        # driver.implicitly_wait(5)

        # Drag slider bar to leftmost to get most bonus rate
        dragsource = driver.find_element_by_css_selector(
            "span[class='ui-slider-handle ui-state-default ui-corner-all'][tabindex='0']")
        dragtarget = driver.find_element_by_css_selector("i[class='fa fa-plus-circle fs18 minus']")
        ActionChains(driver).drag_and_drop(dragsource, dragtarget).perform()

        # Set Bid value to 1
        driver.find_element_by_id('buyamount').clear()
        driver.find_element_by_id('buyamount').send_keys('1')

        # Select bid unit
        # value = 1 : yuan
        # value = 10 : jiao
        # value = 100 : fen
        select = Select(driver.find_element_by_id("selectdollarunit"))
        select.select_by_value("10")

        # Add to bid list
        driver.find_element_by_css_selector("a[class='btn2'][id='seleall']").click()

        # Confirm bid
        driver.find_element_by_css_selector("a[class='btn b3'][id='gamebuy']").click()

        # Handle pop ups after bid confirmation
        # Get last popped up dialog box, that's a bid order confirmation
        confirm_box = driver.find_elements_by_css_selector("button[type='button'][i-id='ok'][class='fix-ui-dialog-autofocus']")[-1]
        confirm_box.click()


    def EndBid(self):
        """
        End biding, clean up.
        :param self: 
        :return: 
        """
        self.logger("Round {round} end, policy:{name}, bid number(s): {numlist}".format( \
            round = self.round \
            name = self.name \
            numlist = str(self.current_bid_list) \
            ))
    def GotoBidPage(self, driver):
        """
        Go to biding page.
        :param self:
        :param driver:
        :return:
        """
        # Click SSC link tag in main page
        driver.find_elements_by_class_name('product_01')[0].click()

        # Cancel POPUP after SSC Link click
        if driver.find_elements_by_class_name('dont-popup')[0].is_displayed():
            driver.find_elements_by_class_name('dont-popup')[0].click()
            driver.find_elements_by_class_name('fa-close')[0].click()