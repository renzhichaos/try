import time
from selenium import webdriver

browser = webdriver.Firefox()
browser.implicitly_wait(5)


def get_img_ids(page, max_page):
    try:
        while page < max_page:
            ids = []
            fw = open("../static/ooxx/" + str(page) + ".html", "w")
            fw.writelines("<html>\n")
            fw.writelines("<head></head>\n")
            fw.writelines("<body>\n<div>\n")
            url = "http://jandan.net/ooxx/page-" + str(page) + "#comments"
            browser.get(url)
            time.sleep(3)
            state = "complete"

            while browser.execute_script("return document.readyState") != state:
                print(browser.execute_script("return document.readyState"))
                time.sleep(3)
            else:
                elements = browser.find_elements_by_xpath("//a[@class='view_img_link']")
                for element in elements:
                    ids.append(element.get_property("href"))
                    fw.writelines("<p><img src='"+element.get_property("href")+"'></p>\n")

            print("第"+str(page)+"页", str(len(ids))+"个图片", ids)
            fw.writelines("</div>\n")
            fw.writelines("</body>\n")
            fw.writelines("</html>")
            fw.close()
            if len(ids) == 0:
                page = page
            else:
                page = page + 1
    except BaseException:
        print("Exception")
    finally:
        browser.close()


