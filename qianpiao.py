import sys
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Qiangpiao():
    def __init__(self, from_station, to_station, depart_time, train_num, passenger):
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.init_my_url = 'https://kyfw.12306.cn/otn/view/index.html'
        self.order_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        # input("出发地：")
        self.from_station = from_station
        # input("目的地：")
        self.to_station = to_station
        # 时间格式必须是M-d的方式
        # input("出发时间：")
        self.depart_time = depart_time
        # input("列车号：")
        self.train_num = train_num
        self.passenger = passenger
        # 获取当前月份
        self.now_month = datetime.date.today().month
        self.driver = webdriver.Chrome()

    def _login(self):
        self.driver.get(self.login_url)
        self.driver.set_window_size(1300, 800)
        # 这里进行手动登录，可以扫码，也可以输入账号密码点击登录
        WebDriverWait(self.driver, 1000).until(EC.url_to_be(self.init_my_url))
        print('登录成功！')

    def _pop_window(self):
        time.sleep(1)
        self.driver.find_element(by=By.XPATH, value='//*[@class="dzp-confirm"]/div[2]/div[3]/a').click()

    def _enter_order_ticket(self):
        action = ActionChains(self.driver)  # 实例化一个动作链对象
        element = self.driver.find_element(by=By.LINK_TEXT, value='车票')
        # 鼠标移动到 '车票' 元素上的中心点
        action.move_to_element(element).perform()
        self.driver.find_element(by=By.XPATH, value='//*[@id="link_for_ticket"]').click()
        self.driver.implicitly_wait(10)

    def _search_ticket(self):
        # 出发地输入
        self.driver.find_element(by=By.ID, value="fromStationText").click()
        self.driver.find_element(by=By.ID, value="fromStationText").send_keys(self.from_station)
        self.driver.find_element(by=By.ID, value="fromStationText").send_keys(Keys.ENTER)
        # 目的地输入
        self.driver.find_element(by=By.ID, value="toStationText").click()
        self.driver.find_element(by=By.ID, value="toStationText").send_keys(self.to_station)
        self.driver.find_element(by=By.ID, value="toStationText").send_keys(Keys.ENTER)
        # 出发日期
        date_tag = self.driver.find_element(by=By.XPATH, value='//*[@id="train_date"]')
        date_tag.click()
        date_tag.clear()
        date_tag.send_keys(self.depart_time)
        time.sleep(1)
        # 等待查询按钮是否可用
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.ID, "query_ticket")))
        # 执行点击事件
        search_btn = self.driver.find_element(by=By.ID, value="query_ticket")
        search_btn.click()
        # 等待查票信息加载
        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="queryLeftTable"]/tr')))

    def _order_ticket(self):
        train_num_list = []  # 列车号列表
        train_num_ele_list = self.driver.find_elements(by=By.XPATH, value='//tr/td[1]/div/div[1]/div/a')  # 列车号元素列表
        for t in train_num_ele_list:  # 遍历列车号元素列表，并把列车号添加到列车号列表
            train_num_list.append(t.text)
        tr_list = self.driver.find_elements(by=By.XPATH,
                                            value='//*[@id="queryLeftTable"]/tr[not(@datatran)]')  # 每一列列车整行信息列表，列车号元素是tr的子元素
        if self.train_num in train_num_list:
            for tr in tr_list:
                train_num = tr.find_element(by=By.XPATH, value="./td[1]/div/div[1]/div/a").text  # 取出元素tr里的列车号
                print("遍历车次：" + train_num)
                if self.train_num == train_num:
                    # 动车二等座余票信息
                    text_1 = tr.find_element(by=By.XPATH, value="./td[4]").text
                    # 火车二等座余票信息
                    text_2 = tr.find_element(by=By.XPATH, value="./td[8]").text
                    if (text_1 == "有" or text_1.isdigit()) or (text_2 == "有" or text_2.isdigit()):
                        # 点击预订按钮
                        order_btn = tr.find_element(by=By.CLASS_NAME, value="btn72")
                        order_btn.click()
                        # 等待订票页面
                        WebDriverWait(self.driver, 1000).until(EC.url_to_be(self.order_url))
                        # 选定乘车人
                        self.driver.find_element(by=By.XPATH,
                                                 value=f'//*[@id="normal_passenger_id"]/li/label[contains(text(),"{self.passenger}")]').click()
                        # 提交订单
                        self.driver.find_element(by=By.ID, value='submitOrder_id').click()
                        time.sleep(2)
                        # 点击确认
                        self.driver.find_element(by=By.ID, value='qr_submit_id').click()
                        print("购票成功！")
                        # 关闭浏览器
                        time.sleep(6)
                        self.driver.quit()
                        sys.exit()
                    else:
                        print("遍历车次：" + train_num + "二等座无票！")
                        break
        else:
            print("无此列车！")

    def run(self):
        # 登录
        self._login()
        # 进入购票页面
        self._enter_order_ticket()
        while True:
            # 查票
            self._search_ticket()
            # 订票
            # my_list = ['G1357', 'G817', 'G1373', 'G1359', 'G4833', 'G1365', 'G1305', 'G1363', 'G1331', 'G4831', 'G1501',
            #            'G1371', 'G2335', 'G1433', 'G1347', 'G1353', 'G1369', 'G4853', 'G1361', 'G1544']
            # 自己去查要买的车次
            my_list = ['G1357', 'G817', 'G1373', 'aabb']
            for i in my_list:
                self.train_num = i
                self._order_ticket()
            # 获取当前时间
            current_time = datetime.datetime.now()
            # 输出当前时间
            print("执行时间：")
            print(current_time)
            time.sleep(10)


# G1357,G817,G1373,G1359,G4833,G1365,G1305,G1363,G1331,G4831,G1501,G1371,G2335,G1433,G1347,G1353,G1369,G4853,G1361
if __name__ == '__main__':
    qiangpiao = Qiangpiao("杭州", "长沙", "2024-02-01", "", "姓名")
    qiangpiao.run()
