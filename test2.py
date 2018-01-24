from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.implicitly_wait(5)
browser.get("https://pages.tmall.com/wow/baihuo/act/trial")
act = ActionChains(browser)
act.key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL, 'a')
