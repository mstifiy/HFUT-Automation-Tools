"""
Automatic tools on official website of HFUT
"""
import os  # 用于计算机的操作
import re  # 用于正则
from selenium.common.exceptions import NoSuchElementException   # 用于处理异常
from selenium.webdriver.common.keys import Keys  # 用于模拟键盘事件
from PIL import Image  # 用于打开图片和对图片处理
from selenium import webdriver  # 用于打开网站
from bs4 import BeautifulSoup  # 用于解析网页
import time  # 代码运行停顿

import ocrImage  # 用于验证码识别

class Login_HFUT:   # 模拟登陆HFUT类

    login_state = 0     # 登陆状态，0为未登陆，1为登陆

    def __init__(self, ishide = 0):     # 初始化，默认浏览器有界面

        if (ishide == 1):

            apt = webdriver.ChromeOptions()      # 创建Chrome参数对象
            apt.headless = True                  # 把Chrome设置成可视化无界面模式
            self.driver = webdriver.Chrome(apt)  # 创建Chrome无界面对象

        else:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()        # 将浏览器最大化显示

        self.find_element = self.driver.find_element_by_css_selector
        self.driver.get('http://my.hfut.edu.cn/')  # 打开登陆页面

    def get_pictures_save(self):

        img = self.find_element('#captchaImg')  # 验证码元素位置
        time.sleep(0.5)
        img.click()  # 点击验证码
        self.driver.save_screenshot('pictures.png')  # 全屏截图
        page_snap_obj = Image.open('pictures.png')
        location = img.location
        size = img.size  # 获取验证码的大小参数
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']
        # 按照验证码的长宽，切割验证码
        # 之所以会出现这个坐标偏差是因为windows系统下电脑设置的显示缩放比例造成的，
        # location获取的坐标是按显示100%时得到的坐标，
        # 而截图所使用的坐标却是需要根据显示缩放比例缩放后对应的图片所确定的，
        # 因此就出现了偏差。解决这个问题有三种方法：
        #   1.修改电脑显示设置为100%。这是最简单的方法；
        #   2.缩放截取到的页面图片，即将截图的size缩放为宽和高都除以缩放比例后的大小；
        #   3.修改Image.crop的参数，将参数元组的四个值都乘以缩放比例。
        image_obj = page_snap_obj.crop((left*1.5, top*1.5, right*1.5, bottom*1.5))
        # image_obj.show()  # 打开切割后的完整验证码
        image_obj.save('captcha.png')
        # self.driver.close()  # 处理完验证码后关闭浏览器

    def login(self, Code, STU_Inf):

            # 获取登陆界面的元素
            un = self.find_element('#username')
            pw = self.find_element('#password')
            # reset = self.find_element('#place1')

            un.send_keys(STU_Inf['un'])      # 输入学号
            pw.send_keys(STU_Inf['pw'])    # 输入密码
            self.input_code(Code)           # 输入验证码

    def input_code(self, Code):     # 输入验证码

        login = self.find_element('#loginForm > table:nth-child(1) > tbody > tr:nth-child(3) > td > input[type=submit]:nth-child(3)')
        cd = self.find_element('#code')
        cd.clear()  # 清空错误的验证码
        time.sleep(1)
        cd.send_keys(Code)
        login.click()
        # 巨坑！这里若不等待，即使成功登陆，也将直接跳过NoSuchElementException异常处理，进行下一次get_pictures_save()函数并报错
        time.sleep(1)
        # 判断是否登陆个人主页
        try:
            identify = self.find_element('#shengFen')
        except NoSuchElementException:
            self.login_state = 0
        else:
            self.login_state = 1

        time.sleep(1)

    # 删除相关文件资源
    def delete_images(self):

        paths = {

            'path1': 'captcha.png',     # 验证码图片路径
            'path2': 'pictures.png',     # 登录界面图片路径
        }

        for path in set(paths.values()):        # 遍历字典中的值
            if os.path.exists(path):    # 如果文件存在
                os.remove(path)         # 删除文件

    def get_driver(self):

        return self.driver          # 返回driver

class Get_resource:

    def __init__(self, _driver):

        self.week = 0
        self.driver = _driver
        self.find_element = self.driver.find_element_by_css_selector

    def go_to_menu(self):

        # educational administration 本科教务
        ea = self.find_element(
            '#pf4631 > div > div.portletContent > table > tbody > tr:nth-child(2) > td:nth-child(1) > table > tbody > tr:nth-child(2) > td > a')
        ea.click()
        time.sleep(1)

        # 点击一个链接，往往会在新的标签页中打开页面。而此时新标签页中的元素不能再定位到。
        handles = self.driver.window_handles  # 获取当前浏览器中全部窗口中的句柄
        self.driver.switch_to.window(handles[1])  # n=1时，定位到当前浏览器窗口的第二个标签页，也就是新标签页

    # 抓取课程表信息
    def get_Schedule(self):

        self.go_to_menu()       # 进入选项菜单

        # 我的课表
        sc = self.find_element('#e-op-area > div > div > div.home-content > div > div:nth-child(4) > div')
        sc.click()
        time.sleep(2)

        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[2])
        html = self.driver.page_source  # 获取课表页面的源代码
        # print(html)
        week_button = self.find_element('body > div.container > div:nth-child(2) > div.col.col-sm-3.week-div-opea > button.btn.btn-primary.week.currWeek')
        week_button.click()     # 点击"本周"按钮
        time.sleep(1)
        # week_inf必须在点击按钮之后获取，否则将出现selenium.common.exceptions.StaleElementReferenceException异常
        week_inf = self.find_element('body > div.container > div:nth-child(2) > div:nth-child(2) > div > div.selectize-input.items.full.has-options.has-items > div')
        self.week = int(week_inf.get_attribute('data-value'))  # 获取本周周次

        soup = BeautifulSoup(html, 'lxml')  # 解析网页 ,解析器为lxml XML解析器
        lessonTable = soup.find_all('tbody')
        lessonList = lessonTable[0].find_all('tr')
        # print(lessonList)
        # 课程信息表
        lessonInfList = []
        # 创建课程信息表
        for item in lessonList:
            lesson = item.find_all('td')
            lessonInfList.append({
                # '序号': lesson[0].text,
                '课程名称': lesson[2].text,
                '课程类型': lesson[5].text,
                '授课教师': lesson[7].text,
                '日期时间地点人员': lesson[8].text,
            })
        # print(lessonInfList)
        return lessonInfList

    # 获取本周课程信息
    def get_Current_Schedule(self):

        Current_lessonList = []
        lessonInfList = self.get_Schedule()

        # 筛选本周的课程
        for lessonInf in lessonInfList:

            Inf = lessonInf['日期时间地点人员']
            week_Inf = re.search('(.*?)周', Inf)

            if (week_Inf != None):
                w = week_Inf.group(0).replace('周', '').split(',')
                for t in w:
                    if (t.endswith(')') == True):
                        # 此处代码不完善，需编写处理单双周课程的情况
                        pass
                    elif (len(t) > 2):
                        fAe = t.split('~')
                        if (int(fAe[0])<= self.week <=int(fAe[1])):
                            lessonInf['state'] = 1      # 对本周有课的课程进行标记，state为1表示有课，0表示无课
                        else:
                            lessonInf['state'] = 0
                    else:
                        if (int(t)==17):
                            lessonInf['state'] = 1
                        else:
                            lessonInf['state'] = 0
            else:
                lessonInf['state'] = 0

        for lessonInf in lessonInfList:         # 打印本周课程
            if (lessonInf['state'] == 1):
                Current_lessonList.append(lessonInf['课程名称']+'\t'+lessonInf['授课教师'])
                print(lessonInf['课程名称']+'\t'+lessonInf['授课教师'])

        return Current_lessonList

    def get_driver(self):

        return self.driver          # 返回driver

class Course_selection:

    def __init__(self, _driver):

        self.select_result = []  # 选课结果
        self.select_state = 0   # 选课状态，初始为未选上
        self.driver = _driver
        self.find_element = self.driver.find_element_by_css_selector

    def go_to_Select_menu(self):
        # educational administration 本科教务
        ea = self.find_element('#pf4631 > div > div.portletContent > table > tbody > tr:nth-child(2) > td:nth-child(1) > table > tbody > tr:nth-child(2) > td > a')
        ea.click()
        time.sleep(1)

        # 点击一个链接，往往会在新的标签页中打开页面。而此时新标签页中的元素不能再定位到。
        handles = self.driver.window_handles  # 获取当前浏览器中全部窗口中的句柄
        self.driver.switch_to.window(handles[1])  # n=1时，定位到当前浏览器窗口的第二个标签页，也就是新标签页

        time.sleep(1)
        # 进入"学生选课"
        select_button = self.find_element('#e-op-area > div > div > div.home-content > div > div:nth-child(5) > div')
        select_button.click()
        time.sleep(1)

        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[2])

    # 选择全校公选课,自动“抢”课
    def select_Public_elective_course(self, _goal_lists):

        goal_lists = _goal_lists

        self.go_to_Select_menu()

        # 点击“进入”
        go_button = self.find_element('body > div > div:nth-child(2) > div > div > div:nth-child(3) > div > h4 > a')
        go_button.click()
        time.sleep(1)
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[3])

        # 获取搜索框
        search_button = self.find_element('#global_filter')

        for lesson in goal_lists:
            # 搜索课程
            # **网站，搜索关键词之间不加空格还搜不出来。。。。。
            search_button.send_keys(lesson)
            time.sleep(0.5)
            # 模拟键盘，键入回车
            search_button.send_keys(Keys.ENTER)

            num_inf = self.find_element('#suitable-lessons-table_info > a')       # 获取匹配页面的课程数
            num = int(re.findall('([0-9]{1,2})', num_inf.text)[1])
            # 若没有此门课程，退出循环
            if(num == 0):
                break

            for item in range(1, num + 1):      # rang(m,n)函数范围为[m,n)！！！

                # 逐项获取"选课"按钮
                select_button = self.find_element('#suitable-lessons-table > tbody > tr:nth-child(' + str(item) + ') > td:nth-child(10) > button')
                time.sleep(1)
                select_button.click()
                # 这个个弹窗加载时间是我用命试出来的。。。
                time.sleep(3)
                # 获取选课结果
                modal_response = self.find_element('body > div.modal.fade.add-response > div > div > div.modal-body > div')

                if (modal_response.text == '选课成功'):
                    # 点击关闭
                    close_modal_button = self.find_element('body > div.modal.fade.add-response.in > div > div > div.modal-footer > button')
                    close_modal_button.click()
                    self.select_state = 1       # 选课状态置1
                    break      # 由于同一门课程只能选一门，因此结束此轮循环

                else:
                    # 点击关闭
                    close_modal_button = self.find_element('body > div.modal.fade.add-response.in > div > div > div.modal-footer > button')
                    close_modal_button.click()

            self.print_Select_Inf(lesson)       # 打印自动选课结果

            time.sleep(2)
            search_button.clear()       # 清除搜索框内容，进行下一门课程的搜索

        return self.select_result       # 返回选课结果

    def print_Select_Inf(self, _lesson):

        if(self.select_state == 1):

            print(_lesson + '\t' + '选课成功')
            self.select_result.append(_lesson + '\t' + '选课成功')
        else:

            print(_lesson + '\t' + '选课失败')
            self.select_result.append(_lesson+'\t'+'选课失败')

    def get_driver(self):

        return self.driver          # 返回driver

def login(Get_stu_Inf):

    login_times = 0     # 尝试登陆次数
    max_times = 1      # 限制最大尝试次数，防止信息错误陷入死循环

    if (Get_stu_Inf['un'] != '' and Get_stu_Inf['pw'] != ''):

        a = Login_HFUT()
        a.get_pictures_save()  # 得到验证码图片
        code = ocrImage.ocr_img('captcha.png')
        # print(code)
        a.login(code, Get_stu_Inf)

        while not a.login_state:  # 验证码错误，登陆未成功
            a.get_pictures_save()
            code = ocrImage.ocr_img('captcha.png')
            a.input_code(code)  # 输入验证码
            login_times = login_times + 1
            if(login_times == max_times):
                break

        a.delete_images()
        if (login_times==max_times):
            a.get_driver().quit()
            return 'Inf maybe wrong! Please check it !'
        else:
            return a.get_driver()

    else:
        return 'ERROR, Information is empty!'       # 返回错误

def select_Course(Get_stu_Inf, plans):

    if (plans==[]):
        return 'ERROR, No Plan to Select!'
    driver = login(Get_stu_Inf)
    if (driver=='ERROR, Information is empty!'):
        return 'ERROR, Information is empty!'
    elif(driver == 'Inf maybe wrong! Please check it !'):
        return driver
    else:
        c = Course_selection(driver)  # 实例化选课工具类
        # 目标课程，将希望作为备选的课程名称关键词加入goals列表
        # 为选课准确性，建议附加筛选条件，通常为开课校区和授课教师等关键词
        goals = plans
        result = c.select_Public_elective_course(goals)  # 进行“抢”课
        c.get_driver().quit()  # 关闭浏览器
        return result

def print_Schedule(Get_stu_Inf):

    driver = login(Get_stu_Inf)
    if(driver == 'ERROR, Information is empty!'):
        return 'ERROR, Information is empty!'
    elif(driver == 'Inf maybe wrong! Please check it !'):
        return driver
    else:
        b = Get_resource(driver)    # 实例化获取资源类
        current_List = b.get_Current_Schedule()    # 获取本周课表信息
        b.get_driver().quit()       # 关闭浏览器
        return current_List
