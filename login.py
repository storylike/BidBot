from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from PIL import Image
from bs4 import BeautifulSoup
import time
import os

chromedriver = "C:\\Program Files (x86)\\Google\\Chrome\Application\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get('')

cookie = driver.get_cookies()

driver.find_element_by_id('login').send_keys('storylike1')
#user = driver.find_element_by_id('pass').text

driver.find_element_by_id('pass').send_keys('Clariion1')
#driver.find.element_by_id('pass').clear()
#password = driver.find_element_by_id('pass').text
#print password

loginform = driver.find_element_by_id('login_form')
formwidth = loginform.size['width']
formheight = loginform.size['height']
X = int(loginform.location_once_scrolled_into_view['x'])
Y = int(loginform.location_once_scrolled_into_view['y'])
left = X
top = Y
right = X + formwidth
bottom = Y + formheight

if os.path.exists('temp\\screenshot.png'):
	os.remove('temp\\screenshot.png')
if os.path.exists('temp\\screenshot_form.png'):
	os.remove('temp\\screenshot_form.png')
time.sleep(5)
driver.get_screenshot_as_file('temp\\screenshot.png')
img = Image.open('temp\\screenshot.png')
imgform = img.crop((left, top, right, bottom))
imgform.save('temp\\screenshot_form.png')
# vcode position relative to form
imgvcode = imgform.crop((84, 203, 148, 222))
imgvcode.show()
vcode = input("vcode is:")
print(vcode)
imgvcode.save('vcodes\\' + str(vcode) + '.png')


driver.find_element_by_id('authnum').send_keys(str(vcode))
driver.find_element_by_id('send-button').click()

time.sleep(5)

#os.system('pause')

# Pop up Confirmation 1
driver.find_element_by_id('btnClose').click()
time.sleep(8)

# Pop up Confirmation 2 
driver.find_elements_by_class_name('ui-dialog-button')[0].click()

time.sleep(3)

# Click SSC link tag in main page
driver.find_elements_by_class_name('product_01')[0].click()

# Cancel POPUP after SSC Link click
if driver.find_elements_by_class_name('dont-popup')[0].is_displayed():
	driver.find_elements_by_class_name('dont-popup')[0].click()
	driver.find_elements_by_class_name('fa-close')[0].click()



# Click BuDingWei
driver.find_element_by_css_selector("a[class='btn b0'][data-bettype='5'][data-subid='1123']").click()

# WuXingYiMa BuDingWei
driver.find_element_by_css_selector("input[name='r0'][type='radio'][class='pointer'][value='2_5_112345']").click()
# Select Bid Number, 5, e.g.
driver.find_element_by_css_selector("a[data-num='5'][class='isNum']").click()

#driver.implicitly_wait(5)

# Drag slider bar to leftmost to get most bonus rate
dragsource = driver.find_element_by_css_selector("span[class='ui-slider-handle ui-state-default ui-corner-all'][tabindex='0']")
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

# er xing
driver.find_element_by_css_selector("a[class='btn b0'][data-bettype='1'][data-subid='12']").click()

# houerzhixuanfushi
driver.find_element_by_css_selector("input[name='r0'][type='radio'][class='pointer'][value='2_1_45']").click()
driver.find_elements_by_css_selector("a[href='javascript:;'][data-num='2']")[0].click()

