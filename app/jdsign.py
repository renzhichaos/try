import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium import webdriver
from io import BytesIO
import pycurl
import datetime
import time
import certifi
import json

from PIL import Image
import pytesseract
import pic

from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Firefox()

useragent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 " \
            "Safari/537.36 "


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
    pic.main('code.png')
    print("自动识别:", text)
    authcode = input("请输入验证码：")
    print(authcode)
    browser.find_element_by_name("authcode").send_keys(authcode)


def login(name, pwd):
    browser.get("https://passport.jd.com/new/login.aspx")
    time.sleep(1)
    browser.find_element_by_class_name("login-tab-r").click()
    browser.find_element_by_name("loginname").send_keys(name)
    browser.find_element_by_name("nloginpwd").click()
    browser.find_element_by_name("nloginpwd").send_keys(pwd)


def login_click():
    browser.switch_to.default_content()
    ishide = str(browser.find_element_by_id("o-authcode").get_attribute("style"))
    print(ishide)

    if ishide == "display: block;":
        validate()
        browser.find_element_by_id("loginsubmit").click()
    else:
        browser.find_element_by_id("loginsubmit").click()
    time.sleep(1)

    browser.switch_to.default_content()
    print(browser.current_url)
    if browser.current_url == "https://www.jd.com/":
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
        print("login success")
        browser.get("https://vip.jd.com/home.html")
        time.sleep(1)
        try:
            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "sign-in")))
            browser.find_element_by_class_name("sign-in").click()
        except Exception:
            print("cannot find sign-in")
        else:
            time.sleep(1)
        browser.get("https://try.jd.com")
        time.sleep(1)
    else:
        print("login validate error!")
        login_click()
    cookie = browser.get_cookies()
    # print(cookie)
    return cookie


def get_activity_ids(page, max_page, get_max, try_type, name, pwd):
    ids = []

    if os.path.exists(name + "jdcookie.txt"):
        print(name + "jdcookie.txt" + '文件存在 ! ')
    else:
        # 打开文件,不存在则创建
        file = open(name + "jdcookie.txt", 'w')
        file.close()
    fr = open(name + "jdcookie.txt")
    jdcookie = fr.read()
    print("jdcookie：" + jdcookie)
    fr.close()

    if get_max == 1:
        urlmax = "https://try.jd.com/activity/getActivityList?page=1&activityState=0&activityType=" + try_type
        print(urlmax)
        browser.get(urlmax)
        max_page = int(browser.find_element_by_xpath("//span[@class='p-skip']//em//b").text)

    print("共" + str(max_page) + "页")

    while page <= max_page:
        url = "https://try.jd.com/activity/getActivityList?page=" + str(
            page) + "&activityState=0&activityType=" + try_type
        browser.get(url)

        href = browser.find_elements_by_xpath("//a[@class='link']")
        hrefs = []
        for element in href:
            hrefs.append(str(element.get_property("href")).replace("https://try.jd.com/", "").replace(".html", ""))
            ids.append(str(element.get_property("href")).replace("https://try.jd.com/", "").replace(".html", ""))
        hrefs.sort()
        activityIds = ",".join(hrefs)
        print("第" + str(page) + "页所有商品Id:" + activityIds)
        getApplyState = "https://try.jd.com/user/getApplyStateByActivityIds?activityIds=" + activityIds
        # print(getApplyState)
        c = pycurl.Curl()
        b = BytesIO()
        c.setopt(pycurl.URL, getApplyState)
        c.setopt(pycurl.REFERER, url)
        c.setopt(pycurl.USERAGENT, useragent)
        c.setopt(pycurl.COOKIE, jdcookie)
        c.setopt(pycurl.CAINFO, certifi.where())
        c.setopt(pycurl.WRITEDATA, b)
        c.perform()
        applyid = b.getvalue().decode('UTF-8')
        # print(applyid)

        if applyid == "":
            print("jdcookie已过期!")
            # try:
            #     sys.exit(0)
            # except TimeoutError:
            #     print('die')
            # finally:
            #     print('out')
            login(name, pwd)
            time.sleep(1)
            jdcookienew = login_click()
            print(jdcookienew)
            it = iter(jdcookienew)
            jdcookie = ""
            for x in it:
                if x == jdcookienew[len(jdcookienew) - 1]:
                    jdcookie = jdcookie + x['name'] + "=" + x['value']
                else:
                    jdcookie = jdcookie + x['name'] + "=" + x['value'] + "; "

            print("new jdcookie:" + jdcookie)

            fw = open(name + "jdcookie.txt", "w")
            fw.write(jdcookie)
            fw.close()

            c.setopt(pycurl.URL, getApplyState)
            c.setopt(pycurl.REFERER, url)
            c.setopt(pycurl.USERAGENT, useragent)
            c.setopt(pycurl.COOKIE, jdcookie)
            c.setopt(pycurl.CAINFO, certifi.where())
            c.setopt(pycurl.WRITEDATA, b)
            c.perform()
            applyid = b.getvalue().decode('UTF-8')
            # print(applyid)

        apd = iter(json.loads(applyid))
        apds = []
        for x in apd:
            apds.append(str(x['activityId']))
            ids.remove(str(x['activityId']))
        apds.sort()
        apdss = ",".join(apds)
        print("第" + str(page) + "页已申商品Id:" + apdss)

        page = page + 1
    ids.sort()
    print("未申请列表：", len(ids), ids)
    idss = iter(ids)
    # browser.close()
    print("开始申请：", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("预计时间:", (5 * len(ids)) / 60, "分钟")
    for id in idss:
        apply = "https://try.jd.com/migrate/apply?activityId=" + id + "&source=0"
        capply = pycurl.Curl()
        bapply = BytesIO()
        capply.setopt(pycurl.URL, apply)
        capply.setopt(pycurl.USERAGENT, useragent)
        capply.setopt(pycurl.COOKIE, jdcookie)
        capply.setopt(pycurl.CAINFO, certifi.where())
        capply.setopt(pycurl.WRITEDATA, bapply)
        capply.perform()
        result = bapply.getvalue().decode('UTF-8')
        print(id + "," + result)
        time.sleep(5)

    print("申请结束!", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def close():
    browser.quit()
