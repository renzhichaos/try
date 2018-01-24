import sys

import pyautogui
import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import ActionChains

browser = webdriver.Firefox()
browser.implicitly_wait(5)


def login(name, pwd):
    browser.get("https://login.taobao.com/member/login.jhtml")
    time.sleep(1)
    browser.find_element_by_class_name("login-switch").click()
    time.sleep(1)
    browser.find_element_by_name("TPL_username").click()
    time.sleep(1)
    browser.find_element_by_name("TPL_username").send_keys(name)
    time.sleep(1)
    browser.find_element_by_name("TPL_password").click()
    time.sleep(1)
    browser.find_element_by_name("TPL_password").send_keys(pwd)
    time.sleep(1)
    ishide = str(browser.find_element_by_id("nocaptcha").get_attribute("style"))
    print(ishide)

    if ishide == "display: block;":
        print("move")
        mm = browser.find_element_by_id("nocaptcha")
        draggable = browser.find_element_by_id("nc_1_n1z")

        act = ActionChains(browser)
        act.click_and_hold(draggable).move_by_offset(270, 0).perform()
        act.release()
        print("over")
        time.sleep(3)
        browser.switch_to.default_content()
        try:
            tt = browser.find_element_by_xpath("//span[@class='nc-lang-cnt']").text
            print(tt)
            if tt == "验证通过":
                browser.find_element_by_id("J_SubmitStatic").click()
                time.sleep(3)
                browser.switch_to.default_content()
                try:
                    browser.switch_to.frame(0)
                    browser.find_element_by_xpath("//ul[@class='check-list']/li[1]").click()
                    browser.find_element_by_id("J_Form").submit()
                    time.sleep(3)
                except selenium.common.exceptions.NoSuchElementException:
                    print("没有点击最近购买验证")
            else:
                try:
                    sys.exit(0)
                except TimeoutError:
                    print('die')
                finally:
                    print('out')
        except selenium.common.exceptions.NoSuchElementException:
            print("no such element")
    else:
        browser.find_element_by_id("J_SubmitStatic").click()
        time.sleep(3)


def get_ids():
    browser.switch_to.default_content()
    browser.get("https://pages.tmall.com/wow/baihuo/act/trial?spm=a1z0i.8295104.300.1")
    act = ActionChains(browser)
    act.send_keys(Keys.END)
    act.send_keys(Keys.END)

    act.send_keys(Keys.END).perform()
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mui-itemcell__item--row"))
    )
    num = browser.find_element_by_id("mallPage").size.get("height")
    print(num)
    get = 0
    item = 0
    ids = []
    while num != get or item == 20:
        item = len(browser.find_elements_by_class_name("mui-itemcell__item--row"))
        num = browser.find_element_by_id("mallPage").size.get("height")
        act.send_keys(Keys.END).perform()
        WebDriverWait(browser, 5).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "mui-itemcell__item--row"))
        )
        get = browser.find_element_by_id("mallPage").size.get("height")
        print(num, get, item)
        hrefs = browser.find_elements_by_class_name("mui-itemcell__item--row")

        for e in hrefs:
            href = e.get_attribute("href")
            if ids.count(href) == 0:
                ids.append(href)
    ids.sort()
    fw = open("tbids.txt", "w")
    fw.write(str(ids))
    fw.close()


def apply():
    fr = open("tbids.txt")
    str_ids = fr.read()
    print("str_ids：" + str_ids)
    fr.close()
    ids = list(eval(str_ids))
    result = ids.copy()
    print(len(ids), ids)
    for page in ids:
        print(page, end=" ,")
        pyautogui.hotkey('ctrl', 't')
        # js = 'window.open("'+page+'");'
        # browser.execute_script(js)
        time.sleep(1)
        handles = browser.window_handles
        if len(handles) == 2:
            browser.switch_to.window(handles[1])
            browser.get(page)
            text = browser.find_element_by_xpath("//*[@class='h5try-ra-button special-none op']").text
            if not(text == "已申请，进店逛逛" or text == "已结束，进店逛逛"):
                element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[button='免费试用']")))
                if element:
                    element.click()
                    print("click element", end=",")
                store = browser.find_element_by_xpath("//div[@class='action']")
                if store.text == "点击收藏店铺":
                    store.click()
                    print("click store", end=",")
                else:
                    print("shop stored", end=",")
                browser.find_element_by_xpath("//div[@class='task-footer']/button").location_once_scrolled_into_view
                submit = browser.find_element_by_xpath("//div[@class='task-footer']/button")
                if submit.text == '提交申请':
                    submit.click()
                    print("click submit", end=",")
                    browser.switch_to.default_content()
                    h3 = browser.find_element_by_xpath("//div[@class='wrap']/h3")
                    if h3.text == "您已申请，请耐心等待审核":
                        print("申请成功")
                        result.remove(page)
                        time.sleep(2)
                        browser.close()
            else:
                print(text)
                time.sleep(2)
                browser.close()
                result.remove(page)

    print(ids)
    print(result)


# get_ids()
login("name", "pwd")
apply()


