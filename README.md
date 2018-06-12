# BidBot
This is an automated robot ordering bids based on python

Steps before playing with BidBot:
1. pip install -r requirement.txt

2. Install PIL
   This is pyhton image library for python version 2.7, for python 3, please use pillow

3. Install pytesser   
   You could download pytesser via: http://code.google.com/p/pytesser/
   Unzip to python2.7 directory, under Lib\site-packages\, add this path to system %PATH% environment variable
   Create __init__.py in above python module directory.
   
4. Download Tesseract OCR engine: http://code.google.com/p/tesseract-ocr/
   Unzip and copy tessdata folder to pytesser folder, replace the original one.

5. Modify pytesser.py, "import Image" -> "from PIL import Image" 


6. If you are playing with Chrome, you may need selenium Chrome driver, which could be downloaded from
	http://chromedriver.storage.googleapis.com/index.html
	The Chrome driver and Chrome browser version mapping table could be found on:
	https://blog.csdn.net/huilan_same/article/details/51896672

