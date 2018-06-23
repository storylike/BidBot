import os
from datetime import datetime, date, time
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from PIL import Image
import time
import random
from config import DATETIMEFMT, BID_URL, GL_ROOT, USER, PASSWORD, CHROME_DRIVER_PATH
from Policies.YFFS import YFFS
from Policies.HEZXFS import HEZXFS
#from pytesser import pytesser


class BidRobot(object):
    """
    BidBot is a automatic biding machine.
    """
    def __init__(self, driver):
        """
        Init method.
        :param self:
        :param driver:
        :return:
        """
        self.root_url = BID_URL
        self.round = 0
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.driver = driver

    def load_page(self, url = BID_URL):
        """
        Load page method.
        :param self:
        :param url:
        :return:
        """
        try:
            self.driver.get(url)
            logger("Get the driver of %s" % self.root_url)
        except Exception:
            logger("Fail to get the driver, because of exceptions.")

    def Refresh(self, driver):
        """
        Refresh the main page.
        :param self:
        :param driver:
        :return:
        """
        driver.refresh()
        time.sleep(5)
        # Now, we are logged in, but need to handle some annoying pop-ups
        # Pop up Confirmation 1
        if self.driver.find_element_by_id('btnClose').is_displayed():
            self.driver.find_element_by_id('btnClose').click()
            time.sleep(3)
        # Pop up Confirmation 2
        if self.driver.find_elements_by_class_name('ui-dialog-button')[0].is_displayed():
            self.driver.find_elements_by_class_name('ui-dialog-button')[0].click()
            time.sleep(3)

    def logger(self, logmsg):
        """
        Logger method of this class.
        :param self:
        :param logmsg:
        :return:
        """
        date_today = time.strftime('%Y-%m-%d')
        logtime = time.strftime(DATETIMEFMT)
        with open('Log\\log_' + date_today + '.txt', 'a+') as log:
            log.write(' '.join([logtime, logmsg, '\n']))
        print(' '.join([logtime, logmsg, '\n']))

    def handle_vcode(self, driver):
        """
        This method handles verification codes.
        :param self:
        :param driver:
        :return:
        """
        # Get login_form
        loginform = driver.find_element_by_id('login_form')
        formwidth = loginform.size['width']
        formheight = loginform.size['height']
        X = int(loginform.location_once_scrolled_into_view['x'])
        Y = int(loginform.location_once_scrolled_into_view['y'])
        left = X
        top = Y
        right = X + formwidth
        bottom = Y + formheight
        # Remove temp image captures in temp dir
        if os.path.exists('temp\\screenshot.png'):
            os.remove('temp\\screenshot.png')
        if os.path.exists('temp\\screenshot_form.png'):
            os.remove('temp\\screenshot_form.png')
        time.sleep(5)
        # Time to capture current screenshots
        if driver.get_screenshot_as_file('temp\\screenshot.png'):
            img = Image.open('temp\\screenshot.png')
            imgform = img.crop((left, top, right, bottom))
            imgform.save('temp\\screenshot_form.png')
            # vcode position relative to form
            imgvcode = imgform.crop((84, 203, 148, 222))
            imgvcode.show()
            vcode = input("vcode is:")
            print(vcode)
            imgvcode.save('vcodes\\' + str(vcode) + '.png')
        else:
            self.logger("Screenshot failed!")
        return vcode

    def login(self, driver, userid=USER, password=PASSWORD):
        """
        This is login method.
        :param self:
        :param driver:
        :param userid:
        :param password:
        :return:
        """

        user = driver.find_element_by_id('login').text
        print(user)
        driver.find_element_by_id('login').send_keys(userid)
        user = driver.find_element_by_id('pass').text

        driver.find_element_by_id('pass').send_keys(password)
        vcode = self.handle_vcode(driver)
        self.logger("Vcode identified as {0}".format(vcode))
        driver.find_element_by_id('authnum').send_keys(vcode)
        driver.find_element_by_id('send-button').click()

        time.sleep(5)
        # Now, we are logged in, but need to handle some annoying pop-ups
        # Pop up Confirmation 1
        driver.find_element_by_id('btnClose').click()
        time.sleep(8)
        # Pop up Confirmation 2
        driver.find_elements_by_class_name('ui-dialog-button')[0].click()
        time.sleep(3)

        self.driver.find_elements_by_class_name('product_01')[0].click()
        time.sleep(5)

        if self.driver.find_elements_by_class_name('dont-popup')[0].is_displayed():
            self.driver.find_elements_by_class_name('dont-popup')[0].click()
            self.driver.find_elements_by_class_name('fa-close')[0].click()

    def SafeLogOut(self, driver):
        """
        This is safe logout method.
        :param self:
        :param driver:
        :return:
        """
        driver.find_element_by_css_selector("a[class='btn_logout btn b2'][id='logout']").click()
        confirm_box = \
        driver.find_elements_by_css_selector("button[type='button'][i-id='ok'][class='fix-ui-dialog-autofocus']")[-1]
        confirm_box.click()
        time.sleep(2)

    def WaitForNextBidCycle(self):
        """
        Wait for next biding cycle.
        :param self:
        :return:
        """
        cur_time = time.strftime('%H:%M:%S')
        if (cur_time > '21:58:00') and (cur_time < '10:00:00'):
            # I'm only focusing on time period of 10:00 - 22.00 every day, with drawing lottery interval being 10 minutes.
            raise InvalidBidTime

    def WaitForBidStart(self):
        """
        Wait for biding cycle starts: skipping period 2:00 - 10:00 everyday.
        :param self:
        :return:
        """
        cur_time = time.strftime('%H:%M:%S')
        need_click = False
        self.logger("Auto_bid: WaitForBidStart...")
        while (cur_time > '02:00:00') and (cur_time < '10:00:00'):
            # I would only work after 10 AM :)
            self.logger("Auto_bid:    Wait 120 seconds...")
            time.sleep(30)
            self.driver.find_element_by_css_selector("a[class='btn b0'][href='#bet/betOrder']").click()
            time.sleep(60)
            self.driver.find_element_by_css_selector("a[class='btn b0'][href='#bet/betPapers']").click()
            time.sleep(30)
            cur_time = time.strftime('%H:%M:%S')
            need_click = True
        if need_click:
            time.sleep(30)
            self.driver.find_element_by_css_selector("a[class='btn b0'][id='nowGP']").click()
            time.sleep(5)

def logger(log_string):
    """
    Logger function for main.
    :param log_string:
    :return:
    """
    date_today = time.strftime('%Y-%m-%d')
    logtime = time.strftime(DATETIMEFMT)
    with open('Log\\log_'+date_today+'.txt', 'a+') as log:
        log.write(' '.join([logtime, log_string, '\n']))

    print(' '.join([logtime, log_string, '\n']))


if __name__ == '__main__':
    """
    This is main loop.
    """
    # Prepare Selenium driver
    chromedriver = CHROME_DRIVER_PATH
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.get(BID_URL)
    cookie = driver.get_cookies()
    print(cookie)
    time.sleep(2)

    Bot = BidRobot(driver)
    Bot.login(driver, USER, PASSWORD)
    # Instantiate HEZXFS
    Policy1 = HEZXFS(driver)
    Policy1.GetTodayData()

    # Instantiate YFFS
    Policy2 = YFFS(driver)
    Policy2.GetTodayData()
    Policy2.CreateBidDict()

    while True:
        # First, we need to check bid time, bid not available during 2:00-10:00 everyday.
        Bot.WaitForBidStart()
        # Reload main page
        #Bot.Refresh(driver)
        ##
        ## Policy 1 handling:
        ##
        '''
        Policy1.GotoBidPage()
        if Policy1.UpdateTodayData():
            Policy1.StartBid()
        # Sleeping between biding policies
        time.sleep(random.randint(10, 15))
        '''
        ##
        ## Policy 2 handling:
        ##
        # Goto biding page
        Policy2.GotoBidPage()
        # Get last biding history
        if Policy2.UpdateTodayData():
            Policy2.UpdateBidDict()
            # Start biding
            Policy2.StartBid()
        # Sleeping between biding policies
        time.sleep(random.randint(10, 15))
        ##
        ## Policy 3 handling:
        ##
        #time.sleep(random.randomint(10, 30))
        # Waiting for next available biding time window
        #Bot.WaitForNextBidCycle(driver)
        '''
        except:
            logger("Main loop break, because of exceptions")
            exit()
        '''

    """
        except exceptions.KeyboardInterrupt:
            loggger("Keyboard interrupt, ending biding procedure!")
            Bot.SafeLogout(self.driver)
            return 1
        except LoginErr:
            logger("Login failed for 3 rounds, this account may has been frozon, please contact JK support!")
            return 2
        except BidingErr:
            logger("Order biding error!")
            return 3
        except InvalidBidTime:
            logger("Please try this BidBot from 10:00 AM - 22:00 PM")
            return 4
        else:
            logger("Unknown error! Stop biding.")
            return 5
    """





















