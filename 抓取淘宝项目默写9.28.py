from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote
from selenium.common.exceptions import TimeoutException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 10)

KEYWORD = 'iPad'

def index_page(page):
    print('正在爬取第', page, '页')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_produts()
    except TimeoutException:
        index_page(page)
        print('爬取第', page, '页失败')


def get_produts():
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        produt = {
            'title': item.find('.title').text(),
            'price': item.find('.price').text(),
            'shop': item.find('.shop').text(),
            'deal': item.find('.deal-cnt').text(),
            'image': item.find('.pic .img').attr('data-src'),
            'location': item.find('.location').text()
        }
        print(produt)

MAX_PAGE = 20

def main():
    for i in range(1, MAX_PAGE+1):
        index_page(i)
    browser.close()


if __name__ == '__main__':
    main()