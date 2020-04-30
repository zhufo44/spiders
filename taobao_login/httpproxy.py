# -*- coding:UTF-8 -*-

# TARGET_URL = 'https://g.alicdn.com/secdev/sufei_data/3.9.0/index.js'
TARGET_URL = 'https://g.alicdn.com/secdev/sufei_data'

# 发现成功的 index.js 和 um.js 中出一段js代码
# 设置 window.navigator.webdriver 为false
INJECT_TEXT = 'Object.defineProperties(navigator,{webdriver:{get:() => false}});'

def response(flow):
    if flow.request.url.startswith(TARGET_URL):
        flow.response.text = INJECT_TEXT + flow.response.text
        print('index注入成功')

    if 'um.js' in flow.request.url:
        flow.response.text = flow.response.text + INJECT_TEXT
        print('um注入成功')