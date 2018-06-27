#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
测试助手
===========================================================================
@Author Bruce He <hebin@comteck.cn>
@Date  2018-06-27
@Version 0.1
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://ss.mis/")

time.sleep(3)
# 登陆
username = driver.find_element_by_xpath('//*[@id="login"]/div[2]/div/div[2]/div[1]/input')
username.clear()
username.send_keys('13012341234')
password = driver.find_element_by_xpath('//*[@id="login"]/div[2]/div/div[2]/div[2]/input')
password.clear()
password.send_keys('123456')
button = driver.find_element_by_xpath('//*[@id="login"]/div[2]/div/div[2]/button')
button.click()

time.sleep(3)
menu1 = driver.find_element_by_xpath('//*[@id="side-bar"]/div[2]/ul/li[1]/div/div/span')
menu1.click()

time.sleep(1)

menu2 = driver.find_element_by_xpath('//*[@id="side-bar"]/div[2]/ul/li[1]/ul/li[1]')
menu2.click()

time.sleep(3)

button1 = driver.find_element_by_xpath('//*[@id="product"]/div[2]/div[1]/div[3]/button[2]')

button1.click()

try:

    alert = WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, '//*[@id="alert"]/div[2]'), '请选择组织')
    )
    print(alert)
finally:
    driver.quit()