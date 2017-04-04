from lxml import etree
import requests
import time
import datetime
import urllib
import jbm

#stocks = ['002108', '600637', '000625', '300182', '600312', '000783', '600340', '000883', '002437', '601009', '000957', '601555', '002100', '300113']
stocks = ['600637', '601555', '002108', '000625', '300182', '000883', '601009',
 '000957', '600312', '002437']
#zqnb(stocks)
#stocks = ['000001']

for code in stocks:
    jstock = jbm.jbm(code)
    jstock.zqyb()