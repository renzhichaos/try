from selenium import webdriver

browser = webdriver.Firefox()
browser.implicitly_wait(5)


def get_img_ids(page, max_page):
    ids = []
    fw = open("jdnet"+ str(page) +".html", "w")
    fw.write("<html>")
    fw.write("<head></head>")
    fw.write("<body><div>")
    while page <= max_page:
        url = "http://jandan.net/pic/page-" + str(page) + "#comments"
        browser.get(url)
        state = "complete"
        while browser.execute_script("return document.readyState") == state:
            elements = browser.find_elements_by_xpath("//a[@class='view_img_link']")
            for element in elements:
                ids.append(element.get_property("href"))

                fw.write("<img src='"+element.get_property("href")+"'>")
            state = "over"
        page = page + 1
    print(len(ids), ids)
    fw.write("</div>")
    fw.write("</body>")
    fw.write("</html>")
    fw.close()


get_img_ids(1, 1)
