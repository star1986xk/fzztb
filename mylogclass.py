import logging
import logging.handlers

class MyLogClass(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        fh = logging.handlers.TimedRotatingFileHandler("my.log", when='d', interval=1,
                                                                backupCount=7)  # 每 1(interval) 天(when) 重写1个文件,保留7(backupCount) 个旧文件；when还可以是Y/m/H/M/S
        fh.suffix = "%Y-%m-%d_%H-%M-%S.log"  # 设置历史文件 后缀
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(lineno)d - %(funcName)s - %(process)d - %(processName)s - %(message)s',
            '%Y/%m/%d %H:%M:%S %p')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

