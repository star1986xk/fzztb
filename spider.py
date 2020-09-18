from mylogclass import MyLogClass
from db_class import db_class
from fzztb_project import FzztbProject
from fzztb_recognizance import FzztbRecognizance
from lyggzy_project import LyggzyProject
from lyggzy_recognizance import LyggzyRecognizance
import configparser
from threading import Thread
from rsa_class import rsa_class

class Spider():
    def __init__(self):
        self.mylog = MyLogClass()
        self.db = db_class(self.mylog)

    def FZGC(self,siteName, domain):
        f = FzztbProject(siteName, domain, self.db, self.mylog)
        f.getIndex(13)

    def FZBZ(self,siteName, domain):
        f = FzztbRecognizance(siteName, domain, self.db, self.mylog)
        f.getIndex(1)

    def LYGC(self,siteName, domain):
        f = LyggzyProject(siteName, domain, self.db, self.mylog)
        f.getIndex(1, 1)
        f.getIndex(2, 1)

    def LYBZ(self,siteName, domain):
        f = LyggzyRecognizance(siteName, domain, self.db, self.mylog)
        f.getStart()


    def run(self):
        tasks = []
        cf = configparser.RawConfigParser()
        cf.read("./config.ini", encoding='utf-8-sig')
        for li in cf['FZGC'].items():
            tasks.append(Thread(target=self.FZGC,args=li))
        for li in cf['FZBZ'].items():
            tasks.append(Thread(target=self.FZBZ,args=li))
        for li in cf['LYGC'].items():
            tasks.append(Thread(target=self.LYGC,args=li))
        for li in cf['LYBZ'].items():
            tasks.append(Thread(target=self.LYBZ,args=li))
        # [t.start() for t in tasks]
        # [t.join() for t in tasks]


        rsa = rsa_class()
        for t in tasks:t.daemon =True
        [t.start() for t in tasks]
        rsa.run()


if __name__ == '__main__':
    S = Spider()
    S.run()