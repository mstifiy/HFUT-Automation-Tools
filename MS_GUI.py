# -*- coding: utf-8 -*-
import time
from tkinter import *

import selenium

import Simulate_HFUT_Tool

class Init_GUI:

    def __init__(self, init_window):
        self.init_window = init_window

    # 设置主窗口
    def set_init_window(self):

        # 窗口设置
        self.init_window.title("录入信息")                       # 窗口名
        self.init_window.geometry('320x160+700+300')                # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        # self.init_window.geometry('1068x681+10+10')
        self.init_window.resizable(False, False)                                      # 禁用缩放，防止用户调整尺寸
        self.init_window["bg"] = "pink"                            # 窗口背景色
        # self.init_window.attributes("-alpha",0.9)                  # 虚化，值越小虚化程度越高

        # 标签
        self.tip_Lable  = Label(self.init_window, text='必须输入相关信息方可进入主界面！' + '\n' + '若输入信息出错，可能将影响您的使用体验哦~')
        self.tip_Lable.grid(row=0, column=0, columnspan=18)
        self.un_data_label = Label(self.init_window, text="账号：")
        self.un_data_label.grid(row=1, column=0, rowspan=2, columnspan=3)
        self.pw_data_label = Label(self.init_window, text="密码：")
        self.pw_data_label.grid(row=3, column=0, rowspan=2, columnspan=3)
        self.version_Label = Label(self.init_window, text='v1.0', font='楷体')
        self.version_Label.place({'x': 270, 'y': 130})


        # 文本框
        self.un_var = StringVar()
        self.un_data_Text = Entry(self.init_window, textvariable=self.un_var)         # 账号输入框
        self.un_data_Text.grid(row=1, column=3, rowspan=2, columnspan=10)       # columnspan参数为合并单元数
        self.pw_var = StringVar()
        self.pw_data_Text = Entry(self.init_window, textvariable=self.pw_var)         # 密码输入框
        self.pw_data_Text['show'] = '*'     # 使用*显示输入的密码
        self.pw_data_Text.grid(row=3, column=3, rowspan=2, columnspan=10)

        # 按钮
        self.submi_button = Button(self.init_window, text="确认", bg="lightblue", width=8, command=self.get_stu_inf)  # 调用内部方法  加()为直接调用
        self.submi_button.grid(row=5, column=10)

    # 获取当前时间
    def get_current_time(self):

        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 获取用户信息
    def get_stu_inf(self):

        un_Inf = self.un_var.get()
        pw_Inf = self.pw_var.get()

        stu_inf['un'] = un_Inf
        stu_inf['pw'] = pw_Inf

        self.write_log_to_file(un_Inf, pw_Inf)      # 生成日志信息
        # 清空输入
        self.un_data_Text.delete(0, 'end')
        self.pw_data_Text.delete(0, 'end')

        self.init_window.destroy()          # 关闭窗口
        app_main()

    # 日志动态打印
    def write_log_to_file(self, un_inf, pw_inf, logmsg=''):   # logmsg参数模式无，可判断用户名与密码格式，产生结果信息

        debug = 1       # 测试阶段数据
        if(debug == 1):
            logmsg = 'Debug'

        current_time = self.get_current_time()
        logmsg_in = str(current_time) + "\t" + 'un:' + un_inf + '\t' + 'pw:' + pw_inf + '\t' + str(logmsg) + "\n"      # 日志格式

        with open('run_log.txt', 'a', encoding='UTF-8') as f:     # with语句来自动调用close()方法，同时解决文件打开异常问题
            f.write(logmsg_in)

class Main_GUI:



    def __init__(self, main_window):

        self.planInf = []
        self.main_window = main_window

    # 设置主窗口
    def set_main_window(self):

        # 窗口设置
        self.main_window.title("小栀")                       # 窗口名
        self.main_window.geometry('320x160+700+300')                # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        # self.init_window.geometry('1068x681+10+10')
        self.main_window.resizable(False, False)                                      # 禁用缩放，防止用户调整尺寸
        self.main_window["bg"] = "pink"                            # 窗口背景色
        # self.init_window.attributes("-alpha",0.9)                  # 虚化，值越小虚化程度越高

        # 菜单
        menubar = Menu(self.main_window)

        fmenu = Menu(menubar)
        fmenu.add_command(label='自动选课', command=self.show_select_result)
        fmenu.add_command(label='打印课表', command=self.show_Schedule)
        fmenu.add_command(label='制定选课方案', command=self.set_select_plan)

        hmenu = Menu(menubar)
        hmenu.add_command(label='使用说明', command=self.show_instructions)
        hmenu.add_command(label='关于作者', command=self.show_me)

        menubar.add_cascade(label="功能", menu=fmenu)  # 添加菜单项
        menubar.add_cascade(label="帮助", menu=hmenu)

        self.main_window['menu'] = menubar  # 将窗口的顶级菜单设置为menu

        # 标签————结果呈现
        self.result = StringVar()
        self.show_area = Label(self.main_window, width=300, height=150, textvariable=self.result)
        self.show_area.pack()

    def show_Schedule(self):

        time.sleep(1)
        self.main_window.withdraw()         # 隐藏窗口
        s = ''
        list = Simulate_HFUT_Tool.print_Schedule(stu_inf)
        self.main_window.deiconify()        # 重新显现
        if(list == 'ERROR, Information is empty!'):
            self.result.set('ERROR, Information is empty!')
        elif(list == 'Inf maybe wrong! Please check it !'):
            self.result.set('Inf maybe wrong! Please check it !')
        else:
            for i in list:
                s = s + i + '\n'
            time.sleep(1)
            self.result.set(s)                   # 操作控件里的内容需使用StringVar对象

    def show_select_result(self):

        time.sleep(1)
        self.main_window.withdraw()  # 隐藏窗口
        s = ''
        try:
            list = Simulate_HFUT_Tool.select_Course(stu_inf, self.planInf)
        except selenium.common.exceptions.NoSuchElementException:       # 官网选课功能未开放，无法进入而导致报错
            list = 'ERROR, Unknown Error!'
        else:
            pass
        self.main_window.deiconify()  # 重新显现

        if (list == 'ERROR, Information is empty!'):
            self.result.set('ERROR, Information is empty!')
        elif(list == 'ERROR, No Plan to Select!'):
             self.result.set('ERROR, No Plan to Select!\nPlease set the plans!')
        elif(list == 'ERROR, Unknown Error!'):
            self.result.set('ERROR, Unknown Error!')
        elif(list == 'Inf maybe wrong! Please check it !'):
            self.result.set('Inf maybe wrong! Please check it !')
        else:
            for i in list:
                 s = s + i + '\n'
            time.sleep(1)
            self.result.set(s)  # 操作控件里的内容需使用StringVar对象

    # 制定选课计划
    def set_select_plan(self):

        self.d = Tk(className='计划制定中...')
        self.d.geometry('320x160+750+350')  # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.d.resizable(False, False)
        self.d["bg"] = "pink"
        self.plan = StringVar()
        self.plan_input = Entry(self.d, textvariable=self.plan)
        plan_label = Label(self.d, text='输入的课程关键字必须以中文逗号（，）为分隔！\n且末尾不能加句号（。）！')
        confirm_button = Button(self.d, text='完成制定', command=self.get_plan)
        plan_label.pack()
        self.plan_input.pack()
        confirm_button.pack()
        self.d.mainloop()

    # 制定
    def get_plan(self):

        Inf = self.plan.get()
        self.planInf = Inf.split('，')
        self.d.destroy()

    # 使用说明书
    def show_instructions(self):
        inst = r'''
    -->开始
    -->在"录入信息"窗口输入正确信息
       账号密码和官网一致
    -->点击"确定"进入主页面
    -->在"功能"菜单中选择功能
       并实现
    Tips：必须输入正确信息，
    在选课前务必制定选课计划，
    必须在官网选课开放时才能正常运行。
    祝您使用愉快~
    '''
        self.result.set(inst)

    # Here is me!
    def show_me(self):
        me = r'''
            应用名称：小栀
            应用分类：实用工具
            应用描述：针对HFUT官网的快捷查询和执行工具
            版本号：v1.0
            作者：MSTIFIY
            2020.6.11  
        '''
        self.result.set(me)

def app_begin():
    # 初始界面
    init_window = Tk()  # 实例化出一个父窗口
    init_gui = Init_GUI(init_window)
    # 设置根窗口默认属性
    init_gui.set_init_window()
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

def app_main():

    mian_window = Tk()
    main_gui = Main_GUI(mian_window)
    # 设置根窗口默认属性
    main_gui.set_main_window()
    mian_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

if __name__ == '__main__':

    stu_inf = {'un': '', 'pw': ''}    # 学生信息
    app_begin()
