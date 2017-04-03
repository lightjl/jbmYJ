from lxml import etree
import requests
import sendMail
import time
import datetime
import getContent
import WorkInTime
import tushare as ts
import urllib
import os

pdStock = ts.get_stock_basics()

class jbm:
    def __init__(self, code):
        self.__code = code
        self.__getContent = getContent.saveToFile()
        self.__name = pdStock.loc[code]['name']

    def isSave(self, filename):
        return self.__getContent.isDownloaded(filename)

    def save(self, filename, text):
        self.__getContent.save(filename, text)

    def sendToKindle(self, filename):
        sendMail.send_attachment_kd(self.__getContent.sub_folder, filename)

    def get_hxgn(self):
        # http://f10.eastmoney.com/f10_v2/OperationsRequired.aspx?code=sh600522&timetip=636267542437023463
        stock = self.__code
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        url = 'http://f10.eastmoney.com/f10_v2/OperationsRequired.aspx?code='
        if stock[0] == '6':
            url += 'sh'
        else:
            url += 'sz'
        url += stock + '&timetip=636267542437023463'
        # print(url)
        html = requests.get(url, headers=headers)
        html.encoding = 'utf-8'
        selector = etree.HTML(html.content)
        hxgn = selector.xpath('//div[@class = "summary"]/p')
        txtHxgn = ''
        for p in hxgn:
            txtHxgn += '    ' + p.xpath('string(.)') + '\n'
            # print(txtHxgn)
        fileName = self.__code + self.__name + '核心题材'
        if not self.isSave(fileName):
            self.save(fileName, txtHxgn)
            self.sendToKindle(fileName)

    def zqyb(self):
        stock = self.__code
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        url = 'http://f10.eastmoney.com/f10_v2/ResearchReport.aspx?code='
        if stock[0] == '6':
            url += 'sh'
        else:
            url += 'sz'
        url += stock + '&timetip=636267680071497248'
        #print(url)
        html = requests.get(url, headers=headers)
        html.encoding = 'utf-8'
        selector = etree.HTML(html.content)
        ybsUrl = selector.xpath('//div[@class = "report"]/a')

        #print(ybsUrl)
        for yburl in ybsUrl:    # todo 增加研报日期

            ybHtml = requests.get(yburl.xpath('./@href')[0], headers=headers)
            ybHtml.encoding = 'utf-8'
            ybSelector = etree.HTML(ybHtml.content)
            txts = ybSelector.xpath('//div[@class = "newsContent"]/p')
            txtYB = ''
            for p in txts:
                txtYB += '    ' + p.xpath('string(.)') + '\r\n'
            if txtYB != '':
                fileName = self.__code + self.__name + ' ' + (yburl.xpath('./text()')[0])
                self.save(fileName, txtYB)
                self.sendToKindle(fileName)
        '''
        txtHxgn = ''
        for p in hxgn:
            txtHxgn += '    ' + p.xpath('string(.)') + '\n'
            # print(txtHxgn)
        fileName = self.__code + self.__name + '核心题材'
        if not self.isSave(fileName):
            self.save(fileName, txtHxgn)
            self.sendToKindle(fileName)
        '''

    def zqnb(self):
        stock = self.__code
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/' + stock + '/page_type/ndbg.phtml'
        html = requests.get(url, headers=headers)
        html.encoding = 'utf-8'
        # req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')

        selector = etree.HTML(html.content)
        name = pdStock.loc[stock]['name']
        # print(url)
        try:
            nbs = (selector.xpath('//div[@class="datelist"]/ul/a'))
            # print(nbs)
            dirName = stock + name
            try:
                os.mkdir('./' + dirName)
            except:
                pass
            for each in nbs:
                target_url = 'http://vip.stock.finance.sina.com.cn' + each.xpath('./@href')[0]
                # print(target_url)

                fileHtml = requests.get(target_url, headers=headers)
                fileHtml.encoding = 'utf-8'
                fSelector = etree.HTML(fileHtml.content)
                # print(fileHtml.content)
                try:
                    fileUrl = fSelector.xpath('//a[contains(text(),"查看PDF公告")]/@href')[0]
                    dataPub = fSelector.xpath('//td[contains(text(),"公告日期")]/text()')[0]

                    fileName = (name + str(int(dataPub.split(':')[1].split('-')[0]) - 1) + '年报')

                    local = './' + dirName + '/' + fileName + '.pdf'
                    if not os.path.isfile(local):
                        # print(local)
                        urllib.request.urlretrieve(fileUrl, local, None)
                except:
                    print('PDF失效;' + fileUrl)
                    continue
        except:
            print('年报列表页面编码错误;' + url)

    def zq3jbNearest(self):
        stock = self.__code
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_BulletinSan/stockid/' + stock + '/page_type/sjdbg.phtml'
        html = requests.get(url, headers=headers)
        html.encoding = 'utf-8'
        # req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')

        selector = etree.HTML(html.content)
        name = pdStock.loc[stock]['name']
        # print(url)
        try:
            jd3b = (selector.xpath('//div[@class="datelist"]/ul/a')[0])
            # print(nbs)
            dirName = stock + name
            try:
                os.mkdir('./' + dirName)
            except:
                pass


            target_url = 'http://vip.stock.finance.sina.com.cn' + jd3b.xpath('./@href')[0]
            # print(target_url)

            fileHtml = requests.get(target_url, headers=headers)
            fileHtml.encoding = 'utf-8'
            fSelector = etree.HTML(fileHtml.content)
            # print(fileHtml.content)
            try:
                fileUrl = fSelector.xpath('//a[contains(text(),"查看PDF公告")]/@href')[0]
                dataPub = fSelector.xpath('//td[contains(text(),"公告日期")]/text()')[0]

                fileName = (name + str(int(dataPub.split(':')[1].split('-')[0])) + '年3季报')

                local = './' + dirName + '/' + fileName + '.pdf'
                if not os.path.isfile(local):
                    # print(local)
                    urllib.request.urlretrieve(fileUrl, local, None)
            except:
                print('PDF失效;' + fileUrl)
        except:
            print('3季度报列表页面编码错误;' + url)