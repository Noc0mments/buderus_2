from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import time
import sqlite3



url_main="https://etk.bosch-plus.ru/app-www/#" #29
options = Options()
# options.headless = True
driver = webdriver.Firefox(options=options, executable_path='e:\pythonProject\geckodriver.exe')
db=sqlite3.connect(r"db\buderus.db")
cur=db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS category (
            id int PRIMARY KEY,
            pos text,
            name text,
            url text,
            parrent_id int,
            parrent_type text,
            art text
            )""")
cur.execute("""CREATE TABLE IF NOT EXISTS product (
            id int PRIMARY KEY,
            pos text,
            name text,
            url text,
            parrent_id int,
            parrent_type text,
            art text            
            )""")
cur.execute("""CREATE TABLE IF NOT EXISTS part (
            id int PRIMARY KEY,
            pos text,
            name text,
            url text,
            parrent_id int,
            parrent_type text,
            art text           
            )""")

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

def parse_item(url):
    res = []
    i=0
    driver.get(url)
    time.sleep(3)
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
                res.append([id_sub, "", name_sub, url_sub, id, type, art_sub, 1])
        else:
            block = driver.find_element_by_class_name("b-category").find_elements_by_tag_name("a")
            for elem in block:
                name_sub = elem.get_property("text")
                url_sub = elem.get_property("href")
                id_sub = url_sub.split("#")[1].split("/")[1]
                res.append([id_sub, "", name_sub, url_sub, id, type,"", 1])
    elif type=="product":
        if check_exists_by_class("b-product-groups", driver):
            block = driver.find_element_by_class_name("b-product-groups").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
            for elem in block:
                pos_sub=elem.find_element_by_tag_name("td").text
                name_sub=elem.find_element_by_tag_name("a").get_property("text")
                url_sub=elem.find_element_by_tag_name("a").get_property("href")
                id_sub = url_sub.split("#")[1].split("/")[1]
                res.append([id_sub,pos_sub, name_sub, url_sub, id, type, "", 1])
        else:
            block = driver.find_element_by_class_name("b-product-parts").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
            for elem in block:
                pos_sub=elem.find_element_by_tag_name("td").text
                name_sub=elem.find_elements_by_tag_name("td")[1].text
                art_sub=elem.find_elements_by_tag_name("td")[2].text
                url_sub=elem.find_element_by_tag_name("a").get_property("href")
                id_sub = url_sub.split("#")[1].split("/")[1]
                res.append([id_sub,pos_sub, name_sub, url_sub, id, type, art_sub, 1])
    return res

def parse_category(id):
    n=1
    cat=parse_item(url_main + "category/"+str(id))
    while n>0:
        n=0
        for el in cat:
            print(el)
            if el[7]==1 and el[3].split("#")[1].split("/")[0]=="category":
                el[7]=0
                cat.extend(parse_item(url_main+"category/"+str(el[0])))
    return(cat)

def zapis_cat_to_db(a):
    for elem in a:
        print(elem)
        table=elem[3].split("#")[1].split("/")[0]
        cur.execute(f"INSERT into {table} VALUES(?, ?, ?, ?, ?, ?, ?);",elem[0:-1])
        db.commit()

def zapis_cat_to_db(a):
    for elem in a:
        print(elem)
        table=elem[3].split("#")[1].split("/")[0]
        cur.execute(f"INSERT into {table} VALUES(?, ?, ?, ?, ?, ?, ?);",elem[0:-1])
        db.commit()


def parse_prod():
    prod=cur.execute("SELECT * FROM product").fetchall()
    res_prod=[]
    for el in prod:
        res_prod.extend(parse_item(el[3]))
    n=1
    while n>0:
        n=0
        for el in res_prod:
            if el[7]==1 and el[3].split("#")[1].split("/")[0]=="product":
                el[7]=0
                res_prod.extend(parse_item(url_main+"product/"+str(el[0])))
    return res_prod

# category=(parse_category(29))
# zapis_cat_to_db(category)
zapis_cat_to_db(parse_prod())

cur.close()
driver.quit()