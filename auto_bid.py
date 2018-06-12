import os
from datetime import datetime, date, time
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from PIL import Image
from pytesser import pytesser
import time
from config import DATETIMEFMT, BID_URL, GL_ROOT, USER, PASSWORD


Class BidRobot(object):
    def __init__(self, URL):
        self.root_url = BID_URL
        self.round = 0
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_options=opts)

    def load_page(self, url = self.root_url):
        try:
            self.driver.get(url)
            logger("Get the driver of %s" % self.root_url)
        except Exception, e:
            logger("Fail to get the driver, because of %s." % e)

    def refresh(self, driver):
        driver.refresh()
    def logger(self, logmsg):
        date_today = time.strftime('Y-%m-%d')
        logtime = time.strftime(DATETIMEFMT)
        with open('Log\\log_' + date_today + '.txt', 'a+') as log:
            log.write(' '.join(logtime, log_string))
        print ' '.join(logtime, log_string)
    def handle_vcode(self, driver):
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
        # Capture current screenshot
        if driver.get_screenshot_as_file('temp\\screenshot.png'):
            img = Image.open('temp\\screenshot.png')
            imgform = img.crop((left, top, right, bottom))
            imgform.save('temp\\screenshot_form.png')
            # vcode position relative to form
            imgvcode = imgform.crop((84, 203, 148, 222))
            imgvcode.show()
            vcode = input("vcode is:")
            print vcode
            imgvcode.save('vcodes\\' + str(vcode) + '.png')
        else:
            self.logger("Screenshot failed!")


    def login(self, driver, userid=USER, password=PASSWORD):

        user = driver.find_element_by_id('login').text
        print user
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


    def WaitForNextBidCycle(self):
        cur_time = time.strftime('%H:%M:%S')
        if (cur_time > '21:58:00') and (cur_time < '10:00:00'):
            # I'm only focusing on time period of 10:00 - 22.00 every day, with drawing lottery interval being 10 minutes.
            raise InvalidBidTime




def logger(log_string):
    date_today = time.strftime('Y-%m-%d')
    logtime = time.strftime(DATETIMEFMT)
    with open('Log\\log_'+date_today+'.txt', 'a+') as log:
        log.write(' '.join(logtime, log_string))

    print ' '.join(logtime, log_string)



if __name__ == '__main__':
    # Prepare Selenium driver
    chromedriver = CHROME_DRIVER_PATH
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.get(BID_URL)
    cookie = driver.get_cookies()
    print cookie
    time.sleep(2)

    Bot = BidRobot()
    Bot.login(driver, USER, PASSWORD)
    Policy1 = YFFS()

    while True:
        try:
        """
            This is the main loop adopting all available policies and bid out orders according to these policies.
        """
            # Reload main page
            Bot.Refresh()

            ##
            ## Policy 1 handling:
            ##
            # Goto biding page
            Policy1.GoToBidPage(driver)
            # Get last biding history
            Policy1.GetHistoryData(driver, )
            data = Policy1.UpdateHistoryData(driver)
            # Predict next bid details according to history data
            predicted = Policy1.Predict(driver)
            # Start biding
            Policy1.StartBid(driver, predicted)

            ##
            ## Policy 2 handling:
            ##

            ##
            ## Policy 3 handling:
            ##


            # Waiting for next available biding time window
            Bot.WaitForNextBidCycle(driver)




        except exceptions.KeyboardInterrupt:
            loggger("Keyboard interrupt, ending biding procedure!")
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






















