from urllib import request
from JSON import loads
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style
from email.mime.text import MIMEText
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.Httpclient import HTTPError
import urllib.parse as parse
import http.cookiejar as cookiejar
import re
import time
import smtplib

# 200 32
# 150 23
# 70  10
init(autoreset=False)


class Colored(object):
    #  前景色:红色  背景色:默认
    def red(self, s):
        return Fore.LIGHTRED_EX + s + Fore.RESET

    #  前景色:绿色  背景色:默认
    def green(self, s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET

    def yellow(self, s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET

    def white(self, s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET

    def blue(self, s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET


class train_ticket_purchase():
    """
        初始化对象属性
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (windows NT 10.0; Win64; x64) AppleWEBKit/537.36 (Khtml, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
        self.opener = self.__get_opener()
        self.username = ""
        self.phone_number = "13781206061"  # 用于占座成功接收短信
        self.receive_email = "wsyjlly@foxmail.com"  # 用于占座成功接收邮件
        self.seatType = "1"  # 1硬座
        self.seat_types_code = ["M", "0", "1", "N", "2", "3", "4", "F", "6", "9"]
        self.ticketType = "1"  # 成人票
        self.query_seats_count = 1  # 查票次数
        self.passengers_name = ""  # 乘车人字符串
        self.seat_list = ["yz_num", "wz_num", "rz_num", "yw_num", "rw_num", "dw_num", "gr_num", "ze_num", "zy_num",
                          "swz_num"]
        self.ticketTypes = {"1": "成人票", "2": "儿童票", "3": "学生票", "4": "残军票"}
        self.seatTypes = {
            "M": "一等座",
            "0": "二等座",
            "1": "硬座",
            "N": "无座",
            "2": "软座",
            "3": "硬卧",
            "4": "软卧",
            "F": "动卧",
            "6": "高等软卧",
            "9": "商务座"
        }
        self.seat_dict = {
            "yz_num": "硬座",
            "wz_num": "无座",
            "rz_num": "软座",
            "yw_num": "硬卧",
            "rw_num": "软卧",
            "dw_num": "动卧",
            "gr_num": "高级软卧",
            "ze_num": "二等座",
            "zy_num": "一等座",
            "swz_num": "商务特等座"
        }

    """
        建立模拟浏览器，模拟浏览器进行cookie存储
    """

    def __get_opener(self):
        c = cookiejar.LWPCookieJar()
        cookie = request.HTTPCookieProcessor(c)
        opener = request.build_opener(cookie)
        request.install_opener(opener)
        return opener

    """
        验证模块：
            1、获取验证图片到本地
            2、将8个图片坐标位置改装成易于输入的1—8的位置编号，输入对应的位置号
            3、发送请求进行后台校验
    """

    # 获取验证图片到本地
    def get_image(self):
        req_catch_image = request.Request('/file/imgs/upload/202301/30/5l2otemnlol.html', 'wb') as f:
        f.write(code_file)


# 图片校验
def verify(self):
    answer = {
        "1": "40,40",
        "2": "110,40",
        "3": "180,40",
        "4": "260,40",
        "5": "40,120",
        "6": "110,120",
        "7": "180,120",
        "8": "260,120",
    }
    print("+----------+----------+----------+----------+")
    print("|    1     |    2     |    3     |    4     |")
    print("|----------|----------|----------|----------|")
    print("|    5     |    6     |    7     |    8     |")
    print("+----------+----------+----------+----------+")
    input_code = input("请在1—8中选择输入验证图片编号，以半角','隔开。(例如：1,3,5):")
    answer_code = ""
    try:
        for i in input_code.split(","):
            answer_code += ("," + answer[i]) if (i is not input_code[0]) else answer[i]
    except:
        print("输入有误,请重新输入！")
        self.verify()
    # 进行图片验证码验证
    req_check = request.Request('https://kyfw.12306.cn/passport/captcha/captcha-check')
    req_check.headers = self.headers
    data = {
        'answer': answer_code,
        'login_site': 'E',
        'rand': 'sjrand'
    }
    data = parse.urlencode(data).encode()
    # 返回验证结果
    check_result = self.opener.open(req_check, data=data).read().decode()  # 读取出来是byts格式，转换为‘utf-8（默认）
    return loads(check_result)


# 验证系统
def sys_verify(self):
    self.get_image()
    verify_result = self.verify()
    while verify_result['result_code'] is not '4':
        print('验证失败，已重新下载图片，请重新验证！')
        self.get_image()
        verify_result = self.verify()
    print("验证通过！")
    return


"""
    登录模块：
        1、输入账号密码，请求服务器
        2、获取apptk授权码
        3、授权通过，成功获取用户信息，将授权信息存储到cookie
"""


def login(self):
    req_login = request.Request('https://kyfw.12306.cn/passport/web/login')
    req_login.headers = self.headers
    name = input("请输入12306帐号:")
    pwd = input("请输入密码:")
    data = {
        'username': name,
        'passWord': pwd,
        'appid': 'otn'
    }
    data = parse.urlencode(data).encode()
    # 返回登录结果
    login_result = self.opener.open(req_login, data=data).read().decode()
    return loads(login_result)


def get_tk(self):
    req = request.Request('https://kyfw.12306.cn/passport/web/auth/uamtk')
    req.headers = self.headers
    data = {
        "appid": "otn"
    }
    data = parse.urlencode(data).encode()
    # 返回登录结果
    result = self.opener.open(req, data=data).read().decode()
    return loads(result)


def auth(self, newapptk):
    req = request.Request('https://kyfw.12306.cn/otn/uamauthclient')
    req.headers = self.headers
    data = {
        "tk": newapptk
    }
    data = parse.urlencode(data).encode()
    # 返回登录结果
    result = self.opener.open(req, data=data).read().decode()
    return loads(result)


# 登陆系统
def sys_login(self):
    self.login()
    result = self.get_tk()
    try:
        result = self.auth(result['newapptk'])
    except:
        print("登录失败,账号或密码错误!")
        self.sys_verify()
        self.sys_login()
    self.username = result["username"]
    print("欢迎用户", result["username"], "您已登录成功！") if result["result_code"] == 0 else print(
        result["result_message"])
    return


"""
    获取站点模块：
        获取所有站点名称与站点码
"""


def __get_city_result(self):
    req_city_code = request.Request(
        'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9093')
    req_city_code.headers = self.headers
    result = self.opener.open(req_city_code).read().decode()
    return result


def get_city_code(self, name):
    result = self.__get_city_result()
    start = result.index(name) + len(name)
    result = result[start + 1:start + 4]
    # print(result)
    return result


def get_station_names(self):
    result = self.__get_city_result()
    stations = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)', result)
    station_codes = dict(stations)
    station_names = dict(zip(station_codes.values(), station_codes.keys()))
    return station_names


"""
    获取余票信息模块：
        1、输入起始站点与乘车时间，请求服务器，查询余票信息
        2、将余票信息进行格式化输出
        3、选择相应车次
"""


def get_tickets(self, from_station, to_station, train_date):
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?'
    data = {
        "leftTicketDTO.train_date": train_date,
        "leftTicketDTO.from_station": from_station,
        "leftTicketDTO.to_station": to_station,
        "purpose_codes": "ADULT"
    }
    req = request.Request(url + parse.urlencode(data))
    req.headers = self.headers
    result = self.opener.open(req).read().decode()
    return loads(result)


def get_ticket_fORMat(self, from_station_name, from_station, to_station_name, to_station, train_date):
    print('为您查询到从', from_station_name, '到', to_station_name, '的余票信息如下：')
    result = self.get_tickets(from_station, to_station, train_date)
    result_list = result['data']['result']

    station_names = self.get_station_names()
    table = PrettyTable(
        ["车次", "出发/到达车站", "出发/到达时间", "历时", "商务座", "一等座", "二等座", "高级软卧", "软卧", "动卧",
         "硬卧", "软座", "硬座", "无座", "其他",
         "备注"])
    for item in result_list:
        name = [
            "station_train_code",
            "from_station_name",
            'start_time',
            "lishi",
            "swz_num",
            "zy_num",
            "ze_num",
            "gr_num",
            "rw_num",
            "dw_num",
            "yw_num",
            "rz_num",
            "yz_num",
            "wz_num",
            "Qt_num",
            "note_num"
        ]
        data = {
            "station_train_code": '',
            "from_station_name": '',
            "to_station_name": '',
            'start_time': '',
            'end': '',
            "lishi": '',
            "swz_num": '',
            "zy_num": '',
            "ze_num": '',
            "dw_num": '',
            "gr_num": '',
            "rw_num": '',
            "yw_num": '',
            "rz_num": '',
            "yz_num": '',
            "wz_num": '',
            "qt_num": '',
            "note_num": ''
        }
        item = item.split('|')  # 用"|"分割字符串
        data['station_train_code'] = item[3]  # 车次在3号位置
        data['from_station_name'] = item[6]  # 始发站信息在6号位置
        data['to_station_name'] = item[7]  # 终点站信息在7号位置
        data['start_time'] = item[8]  # 出发时间信息在8号位置
        data['arrive_time'] = item[9]  # 抵达时间在9号位置
        data['lishi'] = item[10]  # 经历时间在10号位置
        data['swz_num'] = item[32] or item[25]  # 特别注意：商务座在32或25位置
        data['zy_num'] = item[31]  # 一等座信息在31号位置
        data['ze_num'] = item[30]  # 二等座信息在30号位置
        data['gr_num'] = item[21]  # 高级软卧信息在31号位置
        data['rw_num'] = item[23]  # 软卧信息在23号位置
        data['dw_num'] = item[27]  # 动卧信息在27号位置
        data['yw_num'] = item[28]  # 硬卧信息在28号位置
        data['rz_num'] = item[24]  # 软座信息在24号位置
        data['yz_num'] = item[29]  # 硬座信息在29号位置
        data['wz_num'] = item[26]  # 无座信息在26号位置
        data['qt_num'] = item[22]  # 其他信息在22号位置
        data['note_num'] = item[1]  # 备注在1号位置

        color = Colored()  # 创建Colored对象
        data["note_num"] = color.white(item[1])
        # 如果没有信息用'-'代替
        for pos in name:
            if data[pos] == '':
                data[pos] = '-'
        tickets = []
        cont = []
        cont.append(data)
        for x in cont:
            tmp = []
            for y in name:
                if y == "from_station_name":
                    s = color.green(station_names[data['from_station_name']]) + '\n' + color.red(
                        station_names[data["to_station_name"]])
                    tmp.append(s)
                elif y == "start_time":
                    s = color.green(data['start_time']) + '\n' + color.red(data["arrive_time"])
                    tmp.append(s)
                elif y == "station_train_code":
                    s = color.blue(data['station_train_code'])
                    tmp.append(s)
                else:
                    tmp.append(data[y])
            tickets.append(tmp)
        for ticket in tickets:
            table.add_row(ticket)
    print(table)


def get_secret_str(self, from_station, to_station, train_date):
    secret_str = {}
    result = self.get_tickets(from_station, to_station, train_date)
    result = result['data']['result']
    for item in result:
        msg = item.split("|")
        secret_str[msg[3]] = parse.unquote(msg[0])
    # print(secret_str)
    return secret_str


def get_seats(self, station_train_code, from_station, to_station, train_date):
    seats = {}
    result = self.get_tickets(from_station, to_station, train_date)
    result = result['data']['result']
    for item in result:
        item = item.split("|")
        if item[3] == station_train_code:
            seats['swz_num'] = item[32] or item[25]  # 特别注意：商务座在32或25位置
            seats['zy_num'] = item[31]  # 一等座信息在31号位置
            seats['ze_num'] = item[30]  # 二等座信息在30号位置
            seats['gr_num'] = item[21]  # 高级软卧信息在31号位置
            seats['rw_num'] = item[23]  # 软卧信息在23号位置
            seats['dw_num'] = item[27]  # 动卧信息在27号位置
            seats['yw_num'] = item[28]  # 硬卧信息在28号位置
            seats['rz_num'] = item[24]  # 软座信息在24号位置
            seats['yz_num'] = item[29]  # 硬座信息在29号位置
            seats['wz_num'] = item[26]  # 无座信息在26号位置
    return seats


def select_order_details(self):
    print("座位码对照表：")
    print("-----------------------")
    print("|  序号 |  座位类型   |")
    print("|   M   |   一等座    |")
    print("|   0   |   二等座    |")
    print("|   1   |    硬座     |")
    print("|   N   |    无座     |")
    print("|   2   |    软座     |")
    print("|   3   |    硬卧     |")
    print("|   4   |    软卧     |")
    print("|   F   |    动卧     |")
    print("|   6   |  高级软卧   |")
    print("|   9   |   商务座    |")
    print("-----------------------")
    seatType = input("请选择车座类型，enter键默认硬座（例如：1）:")
    if seatType == '':
        self.seatType = "1"
    elif seatType in self.seat_types_code:
        self.seatType = seatType
    else:
        raise Exception("没有对应的车座类型！")

    print("车票类型对照表：")
    print("-----------------------")
    print("|  序号 |  座位类型  |")
    print("|   1   |   成人票   |")
    print("|   2   |   儿童票   |")
    print("|   3   |   学生票   |")
    print("|   4   |   残军票   |")
    print("-----------------------")

    ticketType = input("请选择车票类型，enter键默认成人票（例如：1）:")
    self.ticketType = ticketType if seatType != '' else "1"

    passengers_name = input("请输入乘车人姓名，如有多人，请以英文','隔开（例如：晏沈威,晏文艳）：")
    self.passengers_name = passengers_name if passengers_name != '' else '晏沈威'

    email = input("请输入发送提醒的邮箱（例如：wsyjlly@foxmai.com）：")
    self.receive_email = email if email != '' else "wsyjlly@foxmail.com"

    phone_number = input("请输入发送提醒的手机号（例如：13781206061）：")
    self.phone_number = phone_number if phone_number != '' else "13781206061"


def query_ticket(self, seats, seat_msg):
    if ((seats[seat_msg] == "") | (seats[seat_msg] == "无")):
        print("无", self.seat_dict[seat_msg], "座位！")
        return False
    else:
        print("查询到", seats[seat_msg], self.seat_dict[seat_msg], "座位！")
        return True


def sys_seek_tickets(self):
    while True:
        from_station_name = "郑州"
        from_station_name = input("出发站点(例：郑州):")

        to_station_name = "开封"
        to_station_name = input("到达站点(例：开封):")

        train_date = "2019-02-28"
        train_date = (input("乘车日期(例：2019-02-25):"))

        print("正在为您查询余票信息，请稍等...")
        from_station = self.get_city_code(from_station_name)
        to_station = self.get_city_code(to_station_name)

        self.get_ticket_format(from_station_name, from_station, to_station_name, to_station, train_date)
        if input("输入'1'可继续查询,输入enter键选择车次！") != "1": break

    station_train_code = "K464"
    station_train_code = input("乘车车次(例：K464):")

    # 选择座位类型与车票类型与乘车人姓名
    self.select_order_details()

    while True:
        seats = self.get_seats(station_train_code, from_station, to_station, train_date)
        print('第{}次查票！'.format(self.query_seats_count), seats)
        if (self.seatType == "1"):
            if self.query_ticket(seats, "yz_num") == True: break
        elif (self.seatType == "N"):
            if self.query_ticket(seats, "wz_num") == True: break
        elif (self.seatType == "2"):
            if self.query_ticket(seats, "rz_num") == True: break
        elif (self.seatType == "3"):
            if self.query_ticket(seats, "yw_num") == True: break
        elif (self.seatType == "4"):
            if self.query_ticket(seats, "rw_num") == True: break
        elif (self.seatType == "6"):
            if self.query_ticket(seats, "gr_num") == True: break
        elif (self.seatType == "0"):
            if self.query_ticket(seats, "ze_num") == True: break
        elif (self.seatType == "M"):
            if self.query_ticket(seats, "zy_num") == True: break
        elif (self.seatType == "F"):
            if self.query_ticket(seats, "dw_num") == True: break
        elif (self.seatType == "9"):
            if self.query_ticket(seats, "swz_num") == True: break
        else:
            raise Exception("没有相应车次！")
            break
        self.query_seats_count += 1
        time.sleep(2)

    # 获取相应车次的secret_str
    secret_str = self.get_secret_str(from_station, to_station, train_date)[station_train_code]
    # print(secret_str)
    result = {}
    result["from_station"] = from_station
    result["to_station"] = to_station
    result["train_date"] = train_date
    result["secret_str"] = secret_str
    return result


"""
    订单模块：
        1、注入起始点、日期，车次码信息，提交请求，返回状态信息
        2、获取该车次的详细信息，选择车票类型
        3、获取所有已添加乘客
        4、选择乘车乘客
        5、检查订单信息
        6、确认订单信息，占座成功，下单完成
        7、发送邮件，短信，提醒支付
"""


# {'validateMessagesshowId': '_validatorMessage', 'status': True, 'httpstatus': 200, 'data': 'N', 'messages': [], 'validateMessages': {}}
def get_train_number(self, tickets):
    secret_str = parse.unquote(tickets["secret_str"])
    from_station = tickets["from_station"]
    to_station = tickets["to_station"]
    train_date = tickets["train_date"]
    req = request.Request('https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest')
    req.headers = self.headers
    data = {
        "secretStr": secret_str,
        "train_date": train_date,
        "back_train_date": "",
        "tour_flag": "dc",
        "purpose_codes": "ADULT",
        "query_from_station_name": from_station,
        "query_to_station_name": to_station,
        "undefined": "",
    }
    data = parse.urlencode(data).encode()
    result = self.opener.open(req, data=data).read().decode()
    return loads(result)


# 获取相应车次的信息
def get_train_number_msg(self):
    req = request.Request('https://kyfw.12306.cn/otn/confirmPassenger/initDc')
    req.headers = self.headers
    data = {
        "_json_att": ""
    }
    data = parse.urlencode(data).encode()
    # 返回登录结果
    result = self.opener.open(req, data=data).read().decode()
    try:
        ticketInfoForPassengerForm = re.findall("var ticketInfoForPassengerForm=(.*?);", result)[0].replace("'", '"')
        globalRepeatSubmitToken = re.findall("globalRepeatSubmitToken = '(.*?)'", result)[0]
        key_check_isChange = re.findall("'key_check_isChange':'(.*?)'", result)[0]
    except:
        raise Exception("没有获取到车次信息！")
    ticketInfoForPassengerForm = loads(ticketInfoForPassengerForm)
    leftDetails = ticketInfoForPassengerForm["leftDetails"]
    leftTicketStr = ticketInfoForPassengerForm["leftTicketStr"]
    purpose_codes = ticketInfoForPassengerForm["queryLeftTicketRequestDTO"]["purpose_codes"]
    train_location = ticketInfoForPassengerForm["train_location"]
    print("该车次剩余车票详情如下:")
    for item in leftDetails:
        print("\t", item)
    msg_order_finally_submit = {}
    msg_order_finally_submit["purpose_codes"] = purpose_codes
    msg_order_finally_submit["key_check_isChange"] = key_check_isChange
    msg_order_finally_submit["leftTicketStr"] = leftTicketStr
    msg_order_finally_submit["train_location"] = train_location
    msg_order_finally_submit["token"] = globalRepeatSubmitToken

    return msg_order_finally_submit


# 获取所有已添加乘客
def get_passengers(self, token):
    req = request.Request('https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs')
    req.headers = self.headers
    data = {
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": token
    }
    data = parse.urlencode(data).encode()
    # 返回登录结果
    result = self.opener.open(req, data=data).read().decode()
    result = loads(result)
    normal_passengers = result["data"]["normal_passengers"]
    result = {}
    # print("已添加的乘车人如下：")
    for passenger in normal_passengers:
        result[passenger["passenger_name"]] = passenger
        # if passenger != normal_passengers[len(normal_passengers) - 1]:
        #     print(passenger["passenger_name"] + ",", end='')
        # else:
        #     print(passenger["passenger_name"])
    return result


# 选择乘车人
def select_passenger(self, passengers):
    ps = self.passengers_name
    oldPassengerStr = ''
    passengerTicketStr = ''
    seatType = 1 if self.seatType == "N" else self.seatType
    try:
        ps = ps.split(",")
        for p in ps:
            oldPassengerStr += passengers[p]["passenger_name"] + "," + \
                               passengers[p]["passenger_id_type_code"] + "," + \
                               passengers[p]["passenger_id_no"] + "," + \
                               passengers[p]["passenger_type"] + "_"
            # seatType 座位类型：硬座1软座2硬卧3软卧4
            # passenger_flag 乘客标记：0
            # ticketType 车票类型： 成人票1儿童票2学生票3残军票4
            # passenger_name 乘客姓名
            # passenger_id_type_code 证件类型 中国居民身份证1
            # passenger_id_no 身份证号
            # mobile_no 手机号
            ticketStr = "{},{},{},{},{},{},{},N".format(seatType,
                                                        passengers[p]["passenger_flag"],
                                                        self.ticketType,
                                                        passengers[p]["passenger_name"],
                                                        passengers[p]["passenger_id_type_code"],
                                                        passengers[p]["passenger_id_no"],
                                                        passengers[p]["mobile_no"])
            passengerTicketStr += ticketStr + '_' if p != ps[len(ps) - 1] else ticketStr
    except:
        print("输入有误！")
    result = {}
    result["oldPassengerStr"] = oldPassengerStr
    result["passengerTicketStr"] = passengerTicketStr
    return result


# 检查订单信息
def order_submit(self, msg_passenger, token):
    req = request.Request('https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo')
    req.headers = self.headers
    data = {
        "cancel_flag": "2",
        "bed_level_order_num": "000000000000000000000000000000",
        "passengerTicketStr": msg_passenger["passengerTicketStr"],
        "oldPassengerStr": msg_passenger["oldPassengerStr"],
        "tour_flag": "dc",
        "randCode": "",
        "whatsSelect": "1",
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": token
    }
    data = parse.urlencode(data).encode()
    # 返回登录结果
    result = self.opener.open(req, data=data).read().decode()
    return loads(result)


# 确认订单
def order_ensure(self, msg_passenger, train_number_msg):
    purpose_codes = train_number_msg["purpose_codes"]
    key_check_isChange = train_number_msg["key_check_isChange"]
    leftTicketStr = train_number_msg["leftTicketStr"]
    train_location = train_number_msg["train_location"]
    token = train_number_msg["token"]
    req = request.Request('https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue')
    req.headers = self.headers
    data = {
        "passengerTicketStr": msg_passenger["passengerTicketStr"],
        "oldPassengerStr": msg_passenger["oldPassengerStr"],
        "randCode": "",
        "purpose_codes": purpose_codes,
        "key_check_isChange": key_check_isChange,
        "leftTicketStr": leftTicketStr,
        "train_location": train_location,
        "choose_seats": "",
        "seatDetailType": "000",
        "whatsSelect": "1",
        "roomType": "00",
        "dwAll": "N",
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": token
    }
    data = parse.urlencode(data).encode()
    # 返回登录结果
    result = self.opener.open(req, data=data).read().decode()
    return loads(result)


# 发送email
def send_email(self):
    # 第三方SMTP服务
    mail_host = "smtp.qq.com"
    mail_user = "*******@foxmail.com"
    mail_pass = "****************"

    sender = "wsyjlly@foxmail.com"
    receiver = self.receive_email

    message = MIMEText("席位已锁定，快去支付！")
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = "Python 12306 抢票！"
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(sender, receiver, message.as_string())
        server.close()
        print("邮件发送成功，已提醒用户", receiver, "付款!")
    except Exception as e:
        print("邮件发送失败!", e)


# 发送短信
def send_short_message(self):
    name = self.username
    phone_number = self.phone_number
    seat_type = self.seatTypes[self.seatType]
    ticketType = self.ticketTypes[self.ticketType]
    appid = 1400 ** ** **  # SDK AppID是1400开头
    appkey = "********************************"
    phone_numbers = [phone_number]
    # phone_numbers = ["13781206061", "18337735150", "15660039893"]
    template_id = ** ** **
    sms_sign = "简单点网"

    ssender = SmsSingleSender(appid, appkey)
    params = [name, ticketType, seat_type]
    try:
        result = ssender.send_with_param(86, phone_numbers[0], template_id, params, sign=sms_sign, extend="", ext="")
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
    # print(result)
    if result["errmsg"] == "OK":
        print("短信发送成功，已提醒用户", name, "付款!")


def sys_order(self, tickets):
    # 1、注入起始点、日期，车次码信息，提交请求，返回状态信息
    result = self.get_train_number(tickets)
    if result["status"] == True: print("查询车次信息成功!")
    # 2、获取该车次的详细信息
    train_number_msg = self.get_train_number_msg()
    # 3、获取乘客信息
    passengers = self.get_passengers(train_number_msg["token"])
    # 4、选择乘客
    msg_passenger = self.select_passenger(passengers)
    # print(msg_passenger)
    # 5、下单
    result = self.order_submit(msg_passenger, train_number_msg["token"])
    if result["status"] == True: print("检查订单信息正确，即将确认订单!")

    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # 6、确认订单
    result = self.order_ensure(msg_passenger, train_number_msg)
    if result["status"] == True:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "：下单成功，已占座，请尽快付款!")
        self.send_email()
        self.send_short_message()
    # print(result)
    input("按任意键继续！")


def run(self):
    # 验证码验证
    self.sys_verify()
    # 登录
    self.sys_login()
    # 查余票
    tickets = self.sys_seek_tickets()
    # 下订单
    self.sys_order(tickets)


if __name__ == '__main__':
    while True:
        train_ticket_purchase().run()
