# -*- coding: utf-8 -*-

"""
@author 欧阳秦飞雁
"""
import os
from time import sleep

from selenium import webdriver


class HuoChe(object):
    # 用户名 密码
    username = u"houxiaohuan"
    passwd = u"19dkkk"

    # 车票购买信息,出发地，目的地，日期
    starts = u"阜阳"
    ends = u"深圳"
    # 时间格式2018-02-05
    dtime = u"2019-02-05"

    ###乘客姓名
    users = [u'张学理']

    #测试购票表格网址
    mail_url = "file://" + os.getcwd() + "/123061.html"
    executable_path = os.getcwd() + '/geckodriver'
    wanted_seat_type = [u'二等座',u'硬卧',u'硬座']
    #网址
    # 12306查询URL
    ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
    # 12306登录URL
    login_url = "https://kyfw.12306.cn/otn/login/init"
    # 我的12306URL
    initmy_url = "https://kyfw.12306.cn/otn/view/index.html"
    # 购票URL
    buy_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
    #是否购票成功
    isSuccessBuyTicket = False

    def __init__(self):
        print("Welcome To Use The Tool")
        self.driver = webdriver.Firefox(executable_path=self.executable_path)
        self.driver.set_window_size(1400, 1000)
        # sleep(1)


    def login(self):
        self.driver.get(self.login_url)
        # 填充密码
        self.driver.find_element_by_id("username").send_keys(self.username)
        # sleep(1)
        self.driver.find_element_by_id("password").send_keys(self.passwd)
        print("等待验证码，自行输入....")
        while True:
            sleep(3)
            print("登陆自动化URL" + self.driver.current_url)
            print("登陆成功URL" + self.initmy_url)
            if self.driver.current_url != self.initmy_url:
                sleep(1)
            else:
                break

    def queryTicket(self):
        self.driver.get(self.ticket_url)
        print("begin queyTicket")
        self.driver.add_cookie({'name' : "_jc_save_fromStation", 'value' : cities[self.starts]})
        self.driver.add_cookie({'name' : "_jc_save_toStation", 'value' : cities[self.ends]})
        self.driver.add_cookie({'name' : "_jc_save_fromDate", 'value' : self.dtime})
        #填好缓存后，从新加载网址
        self.driver.get(self.ticket_url)
        xpath = '//*[@id="query_ticket"]'
        queryTicket = self.get_element_by_path(self.driver, xpath)
        if queryTicket:
            try:
                queryTicket.click()  # 点击查询按钮
                print("查询中...")
            except :
                print("查询出错，请定位原因")
        print("end queryTicket")

    def buyTicket(self):
        print("begin buy ticket")
        sleep(1)
        trainInfos = self.get_elements_by_path(self.driver, "//div[@id='t-list']/table/tbody/tr[starts-with(@id,'ticket')]")
        isSucess = False
        if not trainInfos:
            print("query fail.")
            return

        for trainInfo in trainInfos:
            chechi = self.get_element_by_path(trainInfo,".//td[1]/div/div/div/a")
            if chechi:
                print(chechi.text)
                for seat_type in self.wanted_seat_type:
                    if self.has_tickets(trainInfo, seat_type):
                        dinggouButton = self.get_element_by_path(trainInfo, ".//td/a[@class='btn72']")
                        #这样写避免出现because another element  obscures it这个错误
                        self.driver.execute_script("arguments[0].click();", dinggouButton)
                        isSucess = True
                        break;
            if isSucess:
                sleep(2)
                self.confirmTicket()
                break;

        print("end buy ticket")

    def confirmTicket(self):
        while not self.isSuccessBuyTicket:
            try:
                print("开始选择用户....")
                userPaths = "//div/div/div/div/ul[@id='normal_passenger_id']"
                userList = self.get_element_by_path(self.driver, userPaths)
                if userList:
                    for user in self.users:
                        print("选座用户：" + user)
                        userPath = ".//li/label[text()='" + user + "']"
                        checkUser = self.get_element_by_path(userList, userPath)
                        if checkUser:
                            self.get_element_by_path(checkUser, ".//../input").click()

                print("点击成功")
                self.driver.find_element_by_xpath('//div/div/a[@id="submitOrder_id"]').click()
                sleep(1)
                print("确认选座....")
                self.driver.find_element_by_id('qr_submit_id').click()
                sleep(1)
                while True:
                    try:
                        if self.driver.current_url != 'https://kyfw.12306.cn/otn/confirmPassenger/initDc':
                            print("抢票成功，请及时付款")
                            self.isSuccessBuyTicket = True
                            break
                        xpath = '//*[@id="orderResultInfo_id"]/div/span'
                        if self.get_element_by_path(self.driver, xpath):
                            print('抢票失败')
                            break
                    except:
                        continue
            except:
                break


    def has_tickets(self, ele, seat_type):
        path = ".//td[" + str(1 + seat_indexs[seat_type]) + "]/div"
        path1 = ".//td[" + str(1 + seat_indexs[seat_type]) + "]"
        if self.get_element_by_path(ele, path):
            yupiao = self.get_element_by_path(ele, path)
        if self.get_element_by_path(ele, path1):
            yupiao = self.get_element_by_path(ele, path1)
        try :
            if yupiao and (yupiao.text != u"无") and (not yupiao.text.__contains__("--")):
                return yupiao
        except:
            return False

    def get_elements_by_path(self, ele, path):
        try:
            res = ele.find_elements_by_xpath(path)
            if res:
                return res
        except:
            return []

    def get_element_by_path(self, ele, path):
        try:
            res = ele.find_element_by_xpath(path)
            if res:
                return res
        except:
            return ""

seat_indexs = {u'商务座特等座': 1,
               u'一等座': 2,
               u'二等座': 3,
               u'高级软卧': 4,
               u'软卧': 5,
               u'动卧': 6,
               u'硬卧': 7,
               u'软座': 8,
               u'硬座': 9,
               u'无座': 10,
               u'其他': 11}

seat_types = {u'商务座特等座': 9,
               u'一等座': 'M',
               u'二等座': 0,
               u'高级软卧': 6,
               u'软卧': 4,
               u'动卧': 'F',
               u'硬卧': 3,
               u'软座': 2,
               u'硬座': 1,
               u'无座': 1,
               u'其他': 1}


cities = {
    u'天津': '%u5929%u6D25%2CTJP',
    u'南昌': '%u5357%u660C%2CNCG',
    u'桂林': '%u6842%u6797%2CGLZ',
    u'西安': '%u897F%u5B89%2CXAY',
    u'深圳': '%u6DF1%u5733%2CSZQ',
    u'阜阳':'%u961C%u9633%2CFYH'
}

if __name__ == "__main__":
    train = HuoChe()
    train.login()
    while not train.isSuccessBuyTicket:
        train.queryTicket()
        train.buyTicket()
        sleep(10)
