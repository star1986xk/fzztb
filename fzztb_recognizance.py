import configparser
import time

import requests
from copy import deepcopy
from lxml import etree
from settings import *
from mylogclass import MyLogClass
from db_class import db_class


class FzztbRecognizance():

    def __init__(self, siteName, domain, db=None, log=None):
        self.siteName = siteName
        self.domain = domain
        self.db = db
        self.mylog = log

        cf = configparser.RawConfigParser()
        cf.read("./config.ini", encoding='utf-8-sig')
        self.bz_table = cf.get('SQL', 'bz_table')

    def requstPOST(self, url, data,count):
        try:
            response = requests.post(url, json=data, headers=headers, timeout=15)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            count += 1
            if count < 3:
                time.sleep(0.5)
                return self.requstPOST(url, data, count)
            raise e

    def getCompany(self, url, data):
        try:
            result = self.requstPOST(url, data,0)
            for li in result:
                html = etree.HTML(li['modelObj']['remark2'])
                companyList = html.xpath('//*[contains(text(), "公司") or contains(text(), "所") or contains(text(), "队") or contains(text(), "院")]/text()')
                companyList = [li.strip() for li in companyList]
                yield li['modelObj']['seqId'], str(companyList) if companyList else None
        except Exception as e:
            raise e

    def save(self, OBJ_list):
        if OBJ_list:
            result = self.db.insert_many(self.bz_table, OBJ_list)
            if result:
                self.mylog.logger.info('保存！' + str([OBJ['projectName'] for OBJ in OBJ_list]).encode('gbk', 'ignore').decode('gbk'))
                print('保存！' + str([OBJ['projectName'] for OBJ in OBJ_list]).encode('gbk', 'ignore').decode('gbk'))

    def getIndex(self, page):
        data = deepcopy(fzztb_recognizance_index_data)
        data['page']['currentPage'] = page
        index = self.requstPOST(self.domain + fzztb_recognizance_index_url, data,0)
        for li in index['content']:
            recognizance_data = deepcopy(fzztb_recognizance_data)
            recognizance_data['modelObj']['sectionName'] = li['modelObj']['sectionName']
            try:
                for seqid, company in self.getCompany(self.domain + fzztb_recognizance_url, recognizance_data):
                    if self.db.select_count(self.bz_table, [['projectId', '=', seqid],['siteName', '=', self.siteName]]):
                        self.mylog.logger.warning('存在！' + li['modelObj']['sectionName'].encode('gbk', 'ignore').decode('gbk'))
                        print('存在！' + li['modelObj']['sectionName'].encode('gbk', 'ignore').decode('gbk'))
                        continue
                    OBJ = deepcopy(recognizance)
                    OBJ['siteName'] = self.siteName
                    OBJ['domain'] = self.domain
                    OBJ['projectId'] = seqid
                    OBJ['projectName'] = li['modelObj']['sectionName']
                    OBJ['projectNumber'] = li['modelObj']['sectionNumber']
                    OBJ['projectUrl'] = fzztb_recognizance
                    OBJ['company'] = company
                    self.save([OBJ])
            except Exception as e:
                print(e)
        if index['page']['totalPages'] > page:
            page += 1
            return self.getIndex(page)


if __name__ == '__main__':
    siteName = '马尾区建设工程电子招投标交易平台'
    domain = 'http://www.fzztb.com:25000'
    mylog = MyLogClass()
    db = db_class(mylog)
    f = FzztbRecognizance(siteName, domain, db, mylog)
    f.getIndex(1)
