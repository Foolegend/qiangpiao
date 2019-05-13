# -*- coding:utf-8 -*-

"""
@author 欧阳秦飞雁
"""
from splinter.browser import Browser
from time import sleep
import traceback
import time, sys
import os
import urllib3, bs4


class HuoChe(object):
    """docstring for Train"""
    driver_name = ''
    executable_path = ''
    # 用户名 密码
    username = u"houxiaohuanqq"
    passwd = u"19901124a"
    # cookies值自己找
    # 天津%u5929%u6D25%2CTJP 南昌%u5357%u660C%2CNCG 桂林%u6842%u6797%2CGLZ
    starts = u"%u5929%u6D25%2CTJP"
    ends = u"%u5357%u660C%2CNCG"
    # 时间格式2018-02-05
    dtime = u"2018-02-05"
    # 车次,选择第几趟,0则从上之下依次点击
    order = 0
    ###乘客姓名
    users = [u'李国发']
    ##席位
    seat_type=u'二等座'
    seat_type_index = 3
    seat_type_value = 'M'
    """网址"""
    # 12306查询URL
    ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
    # 12306登录URL
    login_url = "https://kyfw.12306.cn/otn/login/init"
    # 我的12306URL
    #initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
    initmy_url = "https://kyfw.12306.cn/otn/view/index.html"
    # 购票URL
    buy = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

    def __init__(self):
        self.driver_name = 'chrome'
        self.executable_path = os.getcwd() + '/chromedriver'
        print("Welcome To Use The Tool")

    def login(self):
        self.driver.visit(self.login_url)
        # 填充密码
        self.driver.fill("loginUserDTO.user_name", self.username)
        # sleep(1)
        self.driver.fill("userDTO.password", self.passwd)
        print("等待验证码，自行输入....")
        while True:
            sleep(3)
            print("登陆自动化URL" + self.driver.url)
            print("登陆成功URL" + self.initmy_url)
            if self.driver.url != self.initmy_url:
                sleep(1)
            else:
                break
    def initSeatType(self, seat_type):
        if seat_type == u'商务座特等座':
          self.seat_type_index = 1
          self.seat_type_value = 9
        elif seat_type == u'一等座':
            self.seat_type_index = 2
            self.seat_type_value = 'M'
        elif seat_type == u'二等座':
            self.seat_type_index = 3
            self.seat_type_value = 0
        elif seat_type == u'高级软卧':
            self.seat_type_index = 4
            self.seat_type_value = 6
        elif seat_type == u'软卧':
            self.seat_type_index = 5
            self.seat_type_value = 4
        elif seat_type == u'动卧':
            self.seat_type_index = 6
            self.seat_type_value = 'F'
        elif seat_type == u'硬卧':
            self.seat_type_index = 7
            self.seat_type_value = 3
        elif seat_type == u'软座':
            self.seat_type_index = 8
            self.seat_type_value = 2
        elif seat_type == u'硬座':
            self.seat_type_index = 9
            self.seat_type_value = 1
        elif seat_type == u'无座':
            self.seat_type_index = 10
            self.seat_type_value = 1
        else:
            self.seat_type_index = 11
            self.seat_type_value = 1

    def start(self):
        self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
        self.driver.driver.set_window_size(1400, 1000)
        self.login()
        # sleep(1)
        self.driver.visit(self.ticket_url)
        try:
            print("购票页面开始....")
            # sleep(1)
            # 加载查询信息
            self.driver.cookies.add({"_jc_save_fromStation": self.starts})
            self.driver.cookies.add({"_jc_save_toStation": self.ends})
            self.driver.cookies.add({"_jc_save_fromDate": self.dtime})

            self.driver.reload()

            count = 0
            if self.order != 0:
                while self.driver.url == self.ticket_url:
                    self.driver.find_bytext(u"查询").click()
                    count += 1
                    print("循环点击查询.... 第 %s 次" % count)
                    # sleep(1)
                    try:
                        self.driver.find_by_xpath("//*[@id='t-list']/table/tbody/tr/td/a[@class='btn72']")[self.order - 1].click()
                    except Exception as e:
                        print(e)
                        print("还没开始预订")
                        continue
            else:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text(u"查询").click()
                    count += 1
                    print("循环点击查询.... 第 %s 次" % count)
                    sleep(2)
                    try:
                        for i in self.driver.find_by_xpath("//*[@id='t-list']/table/tbody/tr/td/a[@class='btn72']"):
                            print('尝试预定')
                            i.click()
                            sleep(1)
                    except Exception as e:
                        print(e)
                        print("预定失败，第 %s 趟车" % count)
                        continue
            print("开始预订....")
            # sleep(1)
            # self.driver.reload()
            sleep(1)
            print("开始选择用户....")
            for user in self.users:
                self.driver.find_by_text(user).last.click()
            print("提交订单....")
            sleep(1)
            # self.driver.find_by_text(self.pz).click()
            # self.driver.find_by_id('').select(self.pz)
            # sleep(1)
            # self.driver.find_by_text(self.xb).click()
            # sleep(1)
            self.driver.find_by_id('submitOrder_id').click()
            print("开始选座...")
            # self.driver.find_by_id('1D').last.click()
            # self.driver.find_by_id('1F').last.click()
            sleep(1.5)
            print("确认选座....")
            self.driver.find_by_text('qr_submit_id').click()

        except Exception as e:
            print(e)


cities = {
    '天津': '%u5929%u6D25%2CTJP',
    '南昌': '%u5357%u660C%2CNCG',
    '桂林': '%u6842%u6797%2CGLZ',
    '西安': '%u897F%u5B89%2CXAY',
    '深圳': '%u6DF1%u5733%2CSZQ'
}

seatT = {"硬卧": "3",
         "软卧": "4",
         "硬座": "1",
         "二等座": "O",
         "一等座": "M",
         "商务座": "9"}




if __name__ == "__main__":
    train = HuoChe()
    # print(sys.argv[1])
    # train.starts = cities[sys.argv[1]]
    # train.ends = cities[sys.argv[2]]
    # train.dtime = sys.argv[3]
    train.starts = cities['天津']
    train.ends = cities['深圳']
    train.dtime =  u"2019-02-05"
    train.initSeatType(train.seat_type)
    train.start()
