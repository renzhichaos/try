import selenium
from selenium import webdriver
import datetime
import time
from PIL import Image
import pytesseract
import pic

browser = webdriver.Firefox()
browser.implicitly_wait(5)


def validate():
    browser.save_screenshot('login.png')  # 截取当前网页，该网页有我们需要的验证码
    imgelement = browser.find_element_by_class_name("verify-code")  # 定位验证码
    location = imgelement.location  # 获取验证码x,y轴坐标
    size = imgelement.size  # 获取验证码的长宽
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
              int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    i = Image.open("login.png")  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save("code.png")
    text = pytesseract.image_to_string(Image.open('code.png'))  # 使用image_to_string识别验证码
    print("自动识别:", text)
    pic.main('code.png')
    authcode = input("请输入验证码：")
    print(authcode)
    browser.find_element_by_name("authcode").send_keys(authcode)


def login(name, pwd):
    browser.get("https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F2017%3Ft%3D2")
    browser.find_element_by_class_name("login-tab-r").click()
    browser.find_element_by_name("loginname").send_keys(name)
    browser.find_element_by_name("nloginpwd").send_keys(pwd)
    time.sleep(1)
    browser.switch_to.default_content()
    ishide = str(browser.find_element_by_id("o-authcode").get_attribute("style"))
    print(ishide)

    if ishide == "display: block;":
        validate()

    browser.find_element_by_id("loginsubmit").click()
    time.sleep(3)
    browser.switch_to.default_content()
    print(browser.current_url)
    if browser.current_url == "https://www.jd.com/2017?t=2":
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
        print("login success")
        browser.get("https://try.jd.com")
        cookie = browser.get_cookies()
        return cookie
    else:
        print("login validate")
        validate()


def get_activity_ids(page, max_page, get_max):
    if get_max == 1:
        urlmax = "https://try.jd.com/activity/getActivityList?page=1&activityState=0&activityType=1"
        browser.get(urlmax)
        max_page = int(browser.find_element_by_xpath("//span[@class='p-skip']//em//b").text)

    print("共" + str(max_page - page + 1) + "页")
    print("预计时间:", (max_page - page + 1) * 20 * 6 / 60, "分钟")
    print("开始申请:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    while page <= max_page:
        ids = []

        url = "https://try.jd.com/activity/getActivityList?page=" + str(page) + "&activityState=0&activityType=1"
        browser.get(url)

        href = browser.find_elements_by_xpath("//a[@class='link']/@href")

        for element in href:
            ids.append(str(element.get_attribute("value")))

        print("第", page, "页:", len(ids), "个:", ids)

        for x in ids:
            browser.get("https:" + x)
            if browser.find_element_by_class_name("state").text == "活动已开始，请快快申请吧！":
                browser.find_element_by_class_name("btn-wrap").click()
                print("未申请, https:" + x + " , click", end=', ')
                time.sleep(1)
                browser.switch_to.default_content()

                try:
                    browser.find_element_by_xpath('//div[@class="ui-dialog-content"]//a[@class="y"]').click()
                    print("关注并申请")
                except selenium.common.exceptions.NoSuchElementException:
                    print("不关注申请")
                time.sleep(5)
            else:
                print("已申请, https:" + x)

        page = page + 1

    print("申请结束!", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# login("name", "pwd")
get_activity_ids(99, 2, 1)
