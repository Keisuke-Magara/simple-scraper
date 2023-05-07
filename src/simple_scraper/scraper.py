import re
from typing import List

import lxml.html
import requests
from lxml.cssselect import CSSSelector

from simple_scraper.element import Element


class Scraper:
    """Scraping websites

    Features
    --------
    Get contents of website by using CSS-Selector or XPATH.
    """

    def __init__(self, url: str) -> None:
        """
        Parameters
        ----------
        url : str
            Target URI (e.g. "https://example.com/")
        """
        self.request_url = url
        self._get_html(self.request_url)

    def _get_html(self, url: str) -> None:
        """[Not Recommendable] Send GET request & parse HTML document of response.

        Normally, please re-create an instance object for each Web page.

        Parameters
        ----------
        url : str
            Target URI (e.g. "https://example.com/")
        """
        self.__response = requests.get(url)
        self.__dom = lxml.html.fromstring(self.__response.content)

    @property
    def response(self) -> requests.Response:
        """Get Response object.

        Returns
        -------
        requests.Response
            Response object of requests library.
        """
        return self.__response

    @property
    def status_code(self) -> int:
        """Get HTTP status code.

        Returns
        -------
        int
            HTTP Status Code (e.g. 200, 404)
        """
        return self.response.status_code

    @property
    def encoding(self):
        return self.response.apparent_encoding

    def by_selector(self, css_selector: str) -> List[Element]:
        matches = self.__dom.cssselect(css_selector)
        ret: List[Element] = []
        for content in matches:
            element = self.__get_element(content)
            ret.append(element)
        return ret

    def by_xpath(self, xpath: str) -> List[Element]:
        # xpathから余計な要素を取り除く
        # xpath = xpath.rstrip('/text()')
        # xpath = xpath.rstrip('/')
        matches = self.__dom.xpath(xpath)
        ret: List[Element] = []
        print(len(matches))
        for content in matches:
            element = self.__get_element(content)
            ret.append(element)
        return ret

    def __get_element(self, html_element):
        HTML_TAG_PATTERN = re.compile(r'<(".*?"|\'.*?\'|[^\'"])*?>')
        element_str = str(lxml.html.tostring(
            html_element, method='html', encoding='unicode'))
        # Replace '<br>' tag to '\n'.
        element_str = element_str.replace('<br>', '\n')
        # Remove other HTML tags.
        element_str = HTML_TAG_PATTERN.sub('', element_str)
        # Remove whitespaces, '\n', '\f', '\t', '\t', '\v' and '\r' from both ends of element_str
        element_str = element_str.strip()
        # element_str = html_element.text_content()
        return Element(element_str, attr=html_element.attrib, parent=html_element.getparent())

    def contains_selector(self, css_selector: str) -> bool:
        return True if self.by_selector(css_selector) else False

    def contains_xpath(self, xpath: str) -> bool:
        return True if self.by_xpath(xpath) else False


if __name__ == '__main__':
    scraper = Scraper("https://travel.rakuten.co.jp/HOTEL/1656/review.html")
    html_str = scraper.response.text
    html_tree = lxml.html.fromstring(html_str)
    print("============ comment area ====================")
    # result1 = html_tree.xpath(
    # "/html/body/div[5]/div/div[4]/div[2]/div[2]/div[3]/div[1]/div[1]/dl/dd/p")
    # result1 = scraper.by_xpath(
    #     "/html/body/div[5]/div/div[4]/div[2]/div[2]/div[3]/div[1]/div[1]/dl/dd/p")
    result1 = scraper.by_selector(
        "#commentArea > div:nth-child(1) > div.commentReputationOne > dl > dd > p")
    print(result1)
    print("================ comment string ===================")
    # result2 = html_tree.xpath(
    # "/html/body/div[5]/div/div[4]/div[2]/div[2]/div[3]/div[1]/div[1]/dl/dd/p")
    result2 = scraper.by_xpath(
        '//*[@id="commentArea"]/div[2]/p/span')
    print(result2)
    # scraper = Scraper("https://lxml.de/xpathxslt.html")
    result3 = scraper.by_xpath(
        '/html/body/div[5]/div/div[4]/div[2]/div[2]/div[3]/div[20]/div[1]/dl[1]/dd/dl/dt[1]')
    print(result3)
