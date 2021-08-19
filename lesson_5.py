from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['db_goods']
goods_bd = db.goods


chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get("https://www.mvideo.ru/")
time.sleep(1)

driver.find_element_by_xpath("//div[@data-init='sticky']").click()

block = driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/../../..")
action = ActionChains(driver)
action.move_to_element(block)
action.perform()

btn = block.find_element_by_class_name("next-btn")

while 'disabled' not in btn.get_attribute('class').split():
    btn.click()
    time.sleep(1)

goods = block.find_elements_by_xpath(".//li")
item = {}
for good in goods:
    item['title'] = good.find_element_by_xpath(".//h3").get_attribute('title')
    item['good_link'] = good.find_element_by_xpath(".//a[contains(@class, 'sel-product-tile-title')]").get_attribute('href')
    item['price'] = good.find_element_by_xpath(".//span[contains(@itemprop, 'price')]").text.replace('&nbsp;', '')

    goods_bd.update_one({'good_link': item['good_link']}, {'$set': item}, upsert=True)


driver.quit()


