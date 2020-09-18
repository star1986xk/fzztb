import configparser
import time

import requests
from copy import deepcopy
from lxml import etree
from settings import *
import re


class LyggzyRecognizance():

    def __init__(self, siteName, domain, db=None, log=None):
        self.siteName = siteName
        self.domain = domain
        self.db = db
        self.mylog = log

        cf = configparser.RawConfigParser()
        cf.read("./config.ini", encoding='utf-8-sig')
        self.bz_table = cf.get('SQL', 'bz_table')

    def requstGET(self, url, count):
        try:
            response = requests.get(url, headers=headers1, timeout=15)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            count += 1
            if count < 3:
                time.sleep(0.5)
                return self.requstGET(url, count)
            raise e

    def requstPOST(self, url, data, count):
        try:
            response = requests.post(url, headers=headers1, data=data, timeout=15)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            count += 1
            if count < 3:
                time.sleep(0.5)
                return self.requstPOST(url, data, count)
            print(e)

    def save(self, OBJ_list):
        if OBJ_list:
            result = self.db.insert_many(self.bz_table, OBJ_list)
            if result:
                self.mylog.logger.info(
                    '保存！' + str([OBJ['projectName'] for OBJ in OBJ_list]).encode('gbk', 'ignore').decode('gbk'))
                print('保存！' + str([OBJ['projectName'] for OBJ in OBJ_list]).encode('gbk', 'ignore').decode('gbk'))

    def getContent(self, text):
        result = re.findall(
            '<tr>\s*?<td class="itemstyle".*?>\s*?(.*?)\s*?</td><td class="itemstyle".*?>\s*?(.*?)\s*?</td><td class="itemstyle".*?>\s*?<div.*?>\s*?(.*?)\s*?</div>\s*?</td><td class="itemstyle".*?>.*?</td><td.*?>.*?</td><td.*?>\s*?.*?\s*?</td><td.*?>\s*?<img.*?"DanWei_List.aspx\?tg=(.*?)",.*?>\s*?</td>\s*?</tr>',
            text, re.S | re.I)
        for li in result:
            if self.db.select_count(self.bz_table, [['projectId', '=', li[-1]], ['siteName', '=', self.siteName]]):
                self.mylog.logger.warning('存在！' + li[2].strip().encode('gbk', 'ignore').decode('gbk'))
                print('存在！' + li[2].strip().encode('gbk', 'ignore').decode('gbk'))
                continue
            try:
                OBJ = deepcopy(recognizance)
                OBJ['siteName'] = self.siteName
                OBJ['domain'] = self.domain
                OBJ['projectId'] = li[-1]
                OBJ['projectName'] = li[2].strip()
                OBJ['projectNumber'] = li[1].strip()
                OBJ['projectUrl'] = lyggzy_recognizance
                company = self.getCompany(self.domain + lyggzy_recognizance_company_url.format(li[-1]))
                OBJ['company'] = company
                self.save([OBJ])
            except Exception as e:
                print(e)

    def getIndex(self, url=None, data=None, page=1, text=None):
        if not text:
            text = self.requstPOST(url, data,0)
        self.getContent(text)
        html = etree.HTML(text)
        pagediv = html.xpath('//div[@id="Pager"]/div[1]')[0]
        pagediv = pagediv.xpath("string(.)")
        total = re.search('总页数：(\d*?) ', pagediv)[1]
        if int(total) > page:
            page += 1
            VIEWSTATE = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            VIEWSTATEGENERATOR = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
            EVENTVALIDATION = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
            data = {
                '__EVENTTARGET': 'Pager',
                '__EVENTARGUMENT': None,
                '__VIEWSTATE': VIEWSTATE,
                '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
                '__EVENTVALIDATION': EVENTVALIDATION,
                'txtProjectName': None,
                'Pager_input': page,
                'Pager': 'go'
            }
            return self.getIndex(url=self.domain + lyggzy_recognizance_index_url, data=data, page=page)

    def getCompany(self, url):
        try:
            text = self.requstGET(url,0)
            if text:
                html = etree.HTML(text)
                Company = html.xpath('//tr/td[2]/text()')
                Company = [li.strip() for li in Company if li.strip() != '单位名称']
                return str(Company) if Company else None
        except Exception as e:
            raise e

    def getStart(self):
        text = self.requstGET(self.domain + lyggzy_recognizance_index_url,0)
        self.getIndex(text=text)

# if __name__ == '__main__':
#     siteName = '龙岩市公共资源交易中心'
#     domain = 'https://www.lyggzy.com.cn'
#     mylog = MyLogClass()
#     db = db_class(mylog)
#     f = LyggzyRecognizance(siteName, domain,db,mylog)
#     f.getStart()
