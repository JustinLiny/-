import requests
import re
import json
import time
from requests.exceptions import RequestException


# 1.获取网页
def get_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
             }
    try:
        req = requests.get(url=url, headers=headers)
        if req.status_code == 200:
            return req.text
    except RequestException as e:
        print(None)



# 2.解析我网页
def parse_page(html):
    partener = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(partener, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            # strip()函数表示移除字符串内指定的字符,此处为空表示移除字符串中的空格
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }

# 3.写入本地
def wirte_page(content):
    with open('result4.txt', 'a', encoding='utf-8')as f:
        # print(type(json.dumps(content)))
        f.write(json.dumps(content,ensure_ascii=False)+ '\n')

# 4.主函数
def main(offset):
    url =  'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_page(url)
    for item in parse_page(html):
        print(item)
        wirte_page(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)

