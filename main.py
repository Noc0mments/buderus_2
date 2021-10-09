from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import time



url_main="https://etk.bosch-plus.ru/app-www/#" #29
options = Options()
# options.headless = True
driver = webdriver.Firefox(options=options, executable_path='g:\pythonProject\geckodriver.exe')

def check_exists_by_class(class_name,drv):
    try:
        drv.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_id(id,drv):
    try:
        drv.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_tag(text,drv):
    try:
        drv.find_element_by_tag_name(text)
    except NoSuchElementException:
        return False
    return True

def parse_prod(url):
    res = []
    print(url)
    i=0
    driver.get(url)
    time.sleep(2)
    type=url.split("#")[1].split("/")[0]
    id=url.split("#")[1].split("/")[1]
    if type=="category":
        if check_exists_by_tag("Table",driver):
            block = driver.find_element_by_tag_name("Table").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
            for elem in block:
                name_sub = elem.find_element_by_tag_name("a").get_property("text")
                url_sub = elem.find_element_by_tag_name("a").get_property("href")
                art_sub = elem.find_element_by_tag_name("td").text
                id_sub = url_sub.split("#")[1].split("/")[1]
                res.append([id_sub, name_sub, url_sub, art_sub, id, type])
        else:
            block = driver.find_element_by_class_name("b-category").find_elements_by_tag_name("a")
            for elem in block:
                name_sub = elem.get_property("text")
                url_sub = elem.get_property("href")
                id_sub = url_sub.split("#")[1].split("/")[1]
                res.append([id_sub, name_sub, url_sub, id, type])
    elif type=="product":
        if check_exists_by_class("b-product-groups", driver):
            block = driver.find_element_by_class_name("b-product-groups").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
            for elem in block:
                pos_sub=elem.find_element_by_tag_name("td").text
                name_sub=elem.find_element_by_tag_name("a").get_property("text")
                url_sub=elem.find_element_by_tag_name("a").get_property("href")
                id_sub = url_sub.split("#")[1].split("/")[1]
                res.append([id_sub,pos_sub, name_sub, url_sub, id, type])
        else:
            block = driver.find_element_by_class_name("b-product-parts").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
            for elem in block:
                pos_sub=elem.find_element_by_tag_name("td").text
                name_sub=elem.find_elements_by_tag_name("td")[1].text
                art_sub=elem.find_elements_by_tag_name("td")[2].text
                url_sub=elem.find_element_by_tag_name("a").get_property("href")
                id_sub = url_sub.split("#")[1].split("/")[1]
                res.append([id_sub,pos_sub, name_sub, url_sub, id, type, art_sub])
    print(res)
    # return res

parse_prod(url_main+"product/4821")
