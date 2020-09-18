import configparser
import time

import requests
from copy import deepcopy
from lxml import etree
from settings import *
import re


class LyggzyProject():

    def __init__(self, siteName, domain, db=None, log=None):
        self.siteName = siteName
        self.domain = domain
        self.db = db
        self.mylog = log

        cf = configparser.RawConfigParser()
        cf.read("./config.ini", encoding='utf-8-sig')
        self.gc_table = cf.get('SQL', 'gc_table')

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
            print(e)

    def save(self, OBJ_list):
        if OBJ_list:
            result = self.db.insert_many(self.gc_table, OBJ_list)
            if result:
                self.mylog.logger.info(
                    '保存！' + str([OBJ['projectName'] for OBJ in OBJ_list]).encode('gbk', 'ignore').decode('gbk'))
                print('保存！' + str([OBJ['projectName'] for OBJ in OBJ_list]).encode('gbk', 'ignore').decode('gbk'))

    def getContent(self, url):
        try:
            content = self.requstGET(self.domain + url, 0)
            html = etree.HTML(content)
            id = re.search('InfoID=(.*?)&', url)[1]
            name = html.xpath('//h3[@class="bigtitle"]/text()')[0].strip()
            annexUrlList = html.xpath('//table[@id="filedown"]//a/@href')
            if self.db.select_count(self.gc_table, [['projectId', '=', id], ['siteName', '=', self.siteName]]):
                self.mylog.logger.warning('存在！' + name.encode('gbk', 'ignore').decode('gbk'))
                print('存在！' + name.encode('gbk', 'ignore').decode('gbk'))
                return None
            OBJ = deepcopy(project)
            OBJ['siteName'] = self.siteName
            OBJ['domain'] = self.domain
            OBJ['projectId'] = id
            OBJ['projectName'] = name
            OBJ['projectNumber'] = id
            OBJ['projectUrl'] = url
            OBJ['annexUrl'] = str([li.replace(self.domain, '') for li in annexUrlList]) if annexUrlList else None
            self.save([OBJ])
        except Exception as e:
            print(e)

    def getIndex(self, num, page):
        index = self.requstGET(self.domain + lyggzy_project_index_url.format(num, page), 0)
        html = etree.HTML(index)
        index_list = html.xpath('//ul[@class="list"]/li/a/@href')
        total = html.xpath('//a[contains(@class,"wb-page-number")]/text()')[0].split('/')[-1]
        for li in index_list:
            self.getContent(li)
        if int(total) > page:
            page += 1
            return self.getIndex(num, page)

# if __name__ == '__main__':
#     siteName = '龙岩市公共资源交易中心'
#     domain = 'https://www.lyggzy.com.cn'
#     mylog = MyLogClass()
#     db = db_class(mylog)
#     f = LyggzyProject(siteName, domain, db, mylog)
#     f.getIndex(1, 1)
#     f.getIndex(2, 1)
