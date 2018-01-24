import sys

import selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium import webdriver
from io import BytesIO
import pycurl
import datetime
import time
import certifi
import json

from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Firefox()

useragent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 " \
            "Safari/537.36 "


def login(name, pwd):
    browser.get("https://passport.jd.com/new/login.aspx")
    time.sleep(1)
    browser.find_element_by_class_name("login-tab-r").click()
    browser.find_element_by_name("loginname").send_keys(name)
    browser.find_element_by_name("nloginpwd").send_keys(pwd)
    browser.find_element_by_id("loginsubmit").click()
    time.sleep(1)
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    print("login success")
    browser.get("https://vip.jd.com/home.html")
    time.sleep(1)
    try:
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "signIn")))
        browser.find_element_by_id("signIn").click()
    except Exception:
        print("cannot find signIn")
    else:
        time.sleep(1)
    browser.get("https://try.jd.com")
    time.sleep(1)
    cookie = browser.get_cookies()
    return cookie


def get_activity_ids(page, max_page, get_max, name, pwd):
    ids = []

    fr = open("jdcookie.txt")
    jdcookie = fr.read()
    print("jdcookie：" + jdcookie)
    fr.close()

    if get_max == 1:
        urlmax = "https://try.jd.com/activity/getActivityList?page=1&activityState=0&activityType=1"
        browser.get(urlmax)
        max_page = int(browser.find_element_by_xpath("//span[@class='p-skip']//em//b").text)

    print("共" + str(max_page) + "页")

    while page <= max_page:
        url = "https://try.jd.com/activity/getActivityList?page=" + str(page) + "&activityState=0&activityType=1"
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
        c.setopt(pycurl.CONNECTTIMEOUT, 5)
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

            jdcookienew = login(name, pwd)
            # print(jdcookienew)

            it = iter(jdcookienew)
            jdcookie = ""
            for x in it:
                if x == jdcookienew[len(jdcookienew) - 1]:
                    jdcookie = jdcookie + x['name'] + "=" + x['value']
                else:
                    jdcookie = jdcookie + x['name'] + "=" + x['value'] + "; "

            print("new jdcookie:" + jdcookie)

            fw = open("jdcookie.txt", "w")
            fw.write(jdcookie)
            fw.close()

            c.setopt(pycurl.CONNECTTIMEOUT, 5)
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
    browser.close()
    print("开始申请：", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("预计时间:", (5 * len(ids)) / 60, "分钟")
    for id in idss:
        apply = "https://try.jd.com/migrate/apply?activityId=" + id + "&source=0"
        capply = pycurl.Curl()
        bapply = BytesIO()
        capply.setopt(pycurl.CONNECTTIMEOUT, 5)
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

