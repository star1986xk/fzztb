import configparser
import time

import requests
from copy import deepcopy
import re
import urllib
from settings import *


class FzztbProject():

    def __init__(self, siteName, domain, db, log):
        self.siteName = siteName
        self.domain = domain
        self.db = db
        self.mylog = log

        cf = configparser.RawConfigParser()
        cf.read("./config.ini", encoding='utf-8-sig')
        self.gc_table = cf.get('SQL', 'gc_table')

    def requstPOST(self, url, data, count):
        try:
            response = requests.post(url, json=data, headers=headers, timeout=15)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            count += 1
            if count < 3:
                time.sleep(0.5)
                return self.requstPOST(url, data, count)
            print(e)

    def requstSN(self, url, data, count):
        try:
            response = requests.post(url, data=data, headers=headers, timeout=15)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            count += 1
            if count < 3:
                time.sleep(0.5)
                return self.requstSN(url, data, count)
            print(e)

    def downFile(self, dirName, sn):
        try:
            self.makedirs(dirName)
            response = requests.get(self.domain + fzztb_down_url.format(sn), stream=True, timeout=15)
            file = response.headers.get('Content-Disposition')
            fileName = re.search('"(.*?)"', file)[1]
            fileName = urllib.parse.unquote(fileName)
            with open(dirName + fileName, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return fzztb_down_url.format(sn)
        except Exception as e:
            print(e)

    def getSn(self, url, projectId, key, com):
        try:
            SnOBJ = self.requstSN(url, projectId, 0)
            file = SnOBJ['modelObj'][key]
            if file:
                sn_list = re.findall(com, file)
                sn_set = deepcopy(set([sn.replace(',', '').strip() for sn in sn_list if sn.replace(',', '').strip()]))
                return sn_set
            return set()
        except Exception as e:
            raise e

    def save(self, OBJ_list):
        if OBJ_list:
            result = self.db.insert_many(self.gc_table, OBJ_list)
            if result:
                self.mylog.logger.info(
                    '保存！' + str([OBJ['projectName'] for OBJ in OBJ_list]).encode('gbk', 'ignore').decode('gbk'))
                print('保存！' + str([OBJ['projectName'] for OBJ in OBJ_list]).encode('gbk', 'ignore').decode('gbk'))

    def getIndex(self, page):
        data = deepcopy(fzztb_project_index_data)
        data['page']['currentPage'] = page
        index = self.requstPOST(self.domain + fzztb_project_index_url, data,0)
        for li in index['content']:
            if self.db.select_count(self.gc_table, [['projectId', '=', li['modelObj']['sectionIds']],
                                                    ['siteName', '=', self.siteName]]):
                self.mylog.logger.warning('存在！' + li['modelObj']['sectionName'].encode('gbk', 'ignore').decode('gbk'))
                print('存在！' + li['modelObj']['sectionName'].encode('gbk', 'ignore').decode('gbk'))
                continue
            try:
                OBJ = deepcopy(project)
                OBJ['siteName'] = self.siteName
                OBJ['domain'] = self.domain
                OBJ['projectId'] = li['modelObj']['sectionIds']
                OBJ['projectName'] = li['modelObj']['sectionName']
                OBJ['projectNumber'] = li['modelObj']['sectionNumbers']
                OBJ['projectUrl'] = fzztb_project_url.format(li['modelObj']['sectionIds'])
                comPdf = re.compile('sn:"(.*?)"')
                comZbf = re.compile('"fileUrl":"(.*?)\\\\')
                sn_setPdf = self.getSn(self.domain + fzztb_pdf_sn_url, OBJ['projectId'], 'remark1', comPdf)
                sn_setZbf = self.getSn(self.domain + fzztb_zbf_sn_url, OBJ['projectId'], 'remark2', comZbf)
                sn_set = sn_setPdf | sn_setZbf
                OBJ['annexUrl'] = str([fzztb_down_url.format(sn) for sn in sn_set]) if sn_set else None
                self.save([OBJ])
            except Exception as e:
                print(e)
        if index['page']['totalPages'] > page:
            page += 1
            return self.getIndex(page)

# if __name__ == '__main__':
#     siteName = '福州建设工程电子招投标交易平台'
#     domain = 'http://www.fzztb.com:25000'
#     domain = 'http://mw.fuebid.com'
#     mylog = MyLogClass()
#     db = db_class(mylog)
#     f = FzztbProject(siteName, domain, db, mylog)
#     f.getIndex(1)
