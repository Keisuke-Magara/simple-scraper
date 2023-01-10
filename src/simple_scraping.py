from dataclasses import dataclass
from typing import Dict, List, Optional

import lxml.html
import requests


@dataclass
class Element:
    text: Optional[str]
    attr: Optional[Dict[str, str]]


class Scraper:
    def __init__(self, url: str) -> None:
        self.request_url = url
        response = requests.get(self.request_url)
        self.html_text = response.text
        self._html_tree = lxml.html.fromstring(self.html_text)

    def from_xpath(self, xpath: str) -> List[Element]:
        # xpathから余計な要素を取り除く
        xpath = xpath.rstrip('/text()')
        xpath = xpath.rstrip('/')
        matches = self._html_tree.xpath(xpath)
        ret: List[Element] = []
        for content in matches:
            element = Element(text=content.text, attr=content.attrib)
            ret.append(element)
        return ret

    def from_selector(self, css_selector: str) -> List[Element]:
        matches = self._html_tree.cssselect(css_selector)
        ret: List[Element] = []
        for content in matches:
            element = Element(text=content.text, attr=content.attrib)
            ret.append(element)
        return ret


if __name__ == '__main__':
    url = "https://www.yahoo.co.jp/"  # スクレイピングしたいWebサイト(適宜変更)
    target_xpath = '/html/body/div/div/main/div[2]/div[1]/article/div/section/div/div[1]/ul'
    # req = requests.get(url)
    # html = req.text
    # dom = lxml.html.fromstring(html)
    # scraped_data = dom.xpath(target_xpath)
    # for index, news in enumerate(scraped_data):
    #     for line in news.text_content().split(" "):
    #         print(line)
    # scraper = Scraper("https://www.yahoo.co.jp/")
    # result = scraper.from_xpath(
    #     '/html/body/div/div/main/div[2]/div[1]/article/div/section/div/div[1]/ul/li[1]/article/a')
    # for i, r in enumerate(result):
    #     p = ''
    #     print(r.href())
    #     # for line in r.text_content():
    #     #     p.join(line)
    #     # print(p)

    # scraper = Scraper("http://www.example.com/")
    # print(scraper.from_xpath("/html/body/div/p[1]/text()"))
    # print(scraper.from_selector("body > div > p:nth-child(2)"))
    a = "/html/body/div/div/main/div[2]/div[1]/article/div/section/div/div[1]/ul/li[1]/article/a/div/div/h1/span"
    b = "/html/body/div/div/main/div[2]/div[1]/article/div/section/div/div[1]/ul/li[2]/article/a/div/div/h1/span"

    scraper = Scraper(url)
    print(scraper.from_xpath(a))
    print(scraper.from_xpath(b))
    print(scraper.from_selector(
        "#tabpanelTopics1 > div > div._2jjSS8r_I9Zd6O9NFJtDN- > ul"))
