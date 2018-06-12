from selenium import webdriver
from PIL import Image
import time
import os
if __name__ == '__main__':
    #PJS_Path = os.path.join(os.getcwd(),os.sep.join('phantomjs-2.1.1','bin','phantomjs'))
    PJS_Path = 'C:\\Codes\\BidBot\\phantomjs-2.1.1\\bin\\phantomjs'
    print PJS_Path
    wbe = webdriver.PhantomJS(executable_path='C:\\Codes\\BidBot\\phantomjs-2.1.1\\bin\\phantomjs')
    wbe.get("")
    element = wbe.find_element_by_xpath('//*[@id="imgCode"]') 
    left = element.location['x']
    top = element.location['y']
    right = element.location['x'] + element.size['width']
    bottom = element.location['y'] + element.size['height']
    index = '1'
    im = Image.open(index +'.png')
    im = im.crop((left, top, right, bottom))
    im.save(index+'.png')