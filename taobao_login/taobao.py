from selenium import webdriver
from time import sleep

driver = webdriver.Chrome()
driver.maximize_window()
# 打开默认是账号密码登录
driver.get('https://login.taobao.com/member/login.jhtml')
sleep(1)
driver.find_element_by_id('fm-login-id').send_keys('username')
sleep(1)
driver.find_element_by_id('fm-login-password').send_keys('password')
sleep(1)
driver.find_element_by_class_name('fm-button').click()

'''
大致请求过程
输入 username 客户端发送ajax请求，验证当前用户及环境是否安全，返回是否弹出验证码

1.对webdriver的检测：index.js um.js
解决：可以通过mitmproxy拦截response，模拟正常请求注入一段js，将navigator.webdriver设置为false
2.为什么要修改chromedriver？

'''
