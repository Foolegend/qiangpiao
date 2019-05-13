# -*- coding: utf-8 -*-

"""
@author 欧阳秦飞雁
"""
import os
import requests
from bs4 import BeautifulSoup
from time import *
from splinter.browser import Browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class HuoChe(object):
    mail_url = "https://mail.126.com/"
    executable_path = os.getcwd() + '/geckodriver'

    def __init__(self):
        rs = requests.get(self.mail_url)
        rs.encoding = "utf-8"
        print(rs.text)
        browser = webdriver.Firefox(executable_path=self.executable_path);
        browser.get(self.mail_url);
        browser.switch_to_frame(2)
        browser.find_element_by_name("email").send_keys("ouyangqinfeiyan")
        browser.find_element_by_name("password").send_keys("6588&woyaofa")
        browser.find_element_by_id("dologin").click()

        if browser.find_elements_by_link_text(u"点此进行验证"):
            print("输入验证码，进行自动校验。")
            sleep(10)
            browser.find_element_by_id("dologin").click()

        print("结束")


        #browser.switch_to_frame(2)
        #print(browser.find_element_by_link_text(u"登录").size)

    def login(self):
        print("text")


if __name__ == "__main__":
    train = HuoChe()
    train.login()
