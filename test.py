from selenium import webdriver
import time
import pic
try:
    import Image
except ImportError:
    from PIL import Image
import pyautogui


print(pyautogui.position())
print(pyautogui.getWindows())
win = pyautogui.getWindow("0").get_position()
print(win)
# pyautogui.click()


# pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
# browser = webdriver.Firefox()
# browser.implicitly_wait(5)
#
#
# browser.get("https://safe.jd.com/findPwd/index.action")
# time.sleep(1)
#
# browser.save_screenshot('login.png')  #截取当前网页，该网页有我们需要的验证码
# imgelement = browser.find_element_by_class_name("ml10")  # 定位验证码
# location = imgelement.location  #获取验证码x,y轴坐标
# size = imgelement.size  #获取验证码的长宽
# rangle = (int(location['x']), int(location['y']), int(location['x']+size['width']), int(location['y']+size['height'])) #写成我们需要截取的位置坐标
# i = Image.open("login.png") #打开截图
# frame4 = i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
# frame4.save('code.png')
# text = pytesseract.image_to_string(Image.open('code.png')) #使用image_to_string识别验证码
# pic.main('code.png')
# print("自动识别:", text)
# authcode = input("请输入验证码：")
# print(authcode)
# browser.find_element_by_name("authCode").send_keys(authcode)




# browser.switch_to.default_content()
# browser.find_element_by_class_name("km-dialog-btn").click()
# time.sleep(3)
# browser.switch_to.default_content()
# browser.find_element_by_class_name("click2slide-btn").click()
# time.sleep(3)
# browser.switch_to.default_content()
# browser.find_element_by_id("password").send_keys("pwd")
# browser.find_element_by_id("btn-submit").click()
# browser.switch_to.default_content()
# browser.find_element_by_xpath("//div[@class='am-check-list  am-flexbox']/div[1]/div[1]").click()
# browser.find_element_by_id("btn-submit").click()
# time.sleep(3)


#
# browser=webdriver.Firefox()
# browser.maximize_window() # 窗口最大化
#
# browser.get('https://www.baidu.com') # 在当前浏览器中访问百度
#
# # 新开一个窗口，通过执行js来新开一个窗口
# js='window.open("https://www.sogou.com");'
# browser.execute_script(js)
#
# print("baidu", browser.current_window_handle) # 输出当前窗口句柄（百度）
# handles = browser.window_handles # 获取当前窗口句柄集合（列表类型）
# print(handles) # 输出句柄集合
#
# for handle in handles:# 切换窗口（切换到搜狗）
#     if handle!=browser.current_window_handle:
#         print('switch to ',handle)
#         browser.switch_to.window(handle)
#         print("sogou", browser.current_window_handle) # 输出当前窗口句柄（搜狗）
#         browser.find_element_by_id("kw").send_keys("haohaoaho")
#
#
# time.sleep(5)
# browser.close() #关闭当前窗口（搜狗）
# time.sleep(5)
# browser.switch_to.window(handles[0]) #切换回百度窗口

# browser.quit()