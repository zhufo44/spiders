import base64
import random
import time, re
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class SlideCode(object):
    def __init__(self):
        chrome_option = webdriver.ChromeOptions()
        # 选择以开发者模式
        chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=chrome_option)
        self.driver.maximize_window()

    def visit_index(self):
        # 输入邮箱和密码
        self.driver.get("https://passport.bilibili.com/login")
        email = WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'login-username')))
        email.clear()
        email.send_keys("email")
        pwd = WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        pwd.clear()
        pwd.send_keys("pwd")

        # 点击登录，弹出滑块验证码
        self.driver.find_element_by_class_name('btn-login').click()
        WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_fullbg')))

        # 进入模拟拖动流程
        self.analog_drag()

    def analog_drag(self):

        # 保存两张图片
        self.save_img('full.jpg', 'geetest_canvas_fullbg')
        self.save_img('cut.jpg','geetest_canvas_bg')
        full_image = Image.open('full.jpg')
        cut_image = Image.open('cut.jpg')

        # 根据两个图片计算距离
        distance = self.get_offset_distance(cut_image, full_image)

        # 开始移动
        self.start_move(distance)

    # 从canvas获取图片
    def save_img(self, img_name, class_name):
        getImgJS = 'return document.getElementsByClassName("' + class_name + '")[0].toDataURL("image/png");'
        img = self.driver.execute_script(getImgJS)
        base64_data_img = img[img.find(',') + 1:]
        image_base = base64.b64decode(base64_data_img)
        file = open(img_name, 'wb')
        file.write(image_base)
        file.close()

    # 判断颜色是否相近
    def is_similar_color(self, x_pixel, y_pixel):
        for i, pixel in enumerate(x_pixel):
            if abs(y_pixel[i] - pixel) > 50:
                return False
        return True

    # 计算距离
    def get_offset_distance(self, cut_image, full_image):
        for x in range(cut_image.width):
            for y in range(cut_image.height):
                cpx = cut_image.getpixel((x, y))
                fpx = full_image.getpixel((x, y))
                if not self.is_similar_color(cpx, fpx):
                    img = cut_image.crop((x, y, x + 50, y + 40))
                    # 保存一下计算出来位置图片，看看是不是缺口部分
                    img.save("1.png")
                    return x

    # def get_track(self,distance):
    #     '''
    #     根据偏移量获取移动轨迹
    #     :param distance: 偏移量
    #     :return: 移动轨迹
    #     '''
    #     # 移动轨迹
    #     tracks = []
    #     # 当前位移
    #     current = 0
    #     # 减速阈值
    #     mid = distance * 4 / 5
    #     # 计算间隔
    #     t = 0.2
    #     # 初速度
    #     v = 0
    #
    #     while current < distance:
    #         if current < mid:
    #             # 加速度为正 2
    #             a = 2
    #         else:
    #             # 加速度为负 3
    #             a = -3
    #         # 初速度 v0
    #         v0 = v
    #         # 当前速度 v=v0+at
    #         v = v0 + a * t
    #         # 移动距离
    #         move = v0 * t + 1 / 2 * a * t * t
    #         # 当前位移
    #         current += move
    #         # 加入轨迹 round 四舍五入
    #         tracks.append(round(move))
    #     jj = 0
    #     for i in tracks:
    #         jj += i
    #     ext = distance - jj
    #     print(ext)
    #     if ext == 0:
    #         pass
    #     elif ext > 0:
    #         for i in range(ext):
    #             tracks.append(1)
    #     else:
    #         for i in range(-ext):
    #             tracks.append(-1)
    #     return tracks

    # def start_move(self,distance):
    #     slider = self.driver.find_element_by_xpath('//div[@class="geetest_slider_button"]')
    #
    #     distance = slider.size.get('width') / 2
    #     distance += 20
    #     tracks = self.get_track(distance)
    #
    #     # 按住滑块
    #     ActionChains(self.driver).click_and_hold(slider).perform()
    #     for x in tracks:
    #         ActionChains(self.driver).move_by_offset(xoffset=x,yoffset=0).perform()
    #     time.sleep(0.5)
    #     ActionChains(self.driver).release().perform()


    # 开始移动
    def start_move(self, distance):
        # 定位滑块
        element = self.driver.find_element_by_xpath('//div[@class="geetest_slider_button"]')

        # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
        distance -= element.size.get('width') / 2
        distance += 25

        # 按下鼠标左键 move_by_offset 从当前坐标移动到 (x,y)
        ActionChains(self.driver).click_and_hold(element).perform()
        time.sleep(0.2)
        while distance > 0:
            if distance > 10:
                # 如果距离大于10，就移动快一点
                span = random.randint(5, 8)
            else:
                # 快到缺口了，就移动慢一点
                span = random.randint(2, 3)
            # 每次移动的速度不一样，看起来卡顿，比较慢
            randy = random.randint(-3,3)
            ActionChains(self.driver).move_by_offset(span, randy).perform()
            distance -= span
            # time.sleep(random.randint(10, 30) / 100)

        ActionChains(self.driver).move_by_offset(distance, 1).perform()
        # 释放鼠标
        ActionChains(self.driver).release(on_element=element).perform()


if __name__ == "__main__":
    bili = SlideCode()
    bili.visit_index()
