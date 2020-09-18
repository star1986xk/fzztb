import subprocess
import time
import configparser


def main():
    cf = configparser.RawConfigParser()
    cf.read("./config.ini", encoding='utf-8-sig')
    t = cf['TIME'].get('time')

    if t:
        print('启动定时：每{}小时开启一次！'.format(t))
        while True:
            subprocess.Popen('./spider.exe')
            time.sleep(60 * 60 * int(t))
    else:
        print('未定时，立即开始！')
        subprocess.Popen('./spider.exe')


if __name__ == '__main__':
    main()
