from crawler import Crawler
from config import Config
import xml.etree.ElementTree as ET

class FieldManager:
    def __init__(self) -> None:
        self._list = []
        self.crawler = Crawler()

    def search(self, keyword):
        """Search for keyword in the list."""
        return

class CountryFieldManager(FieldManager):
    def __init__(self) -> None:
        super().__init__()

    def get_countries_list_online(self):
        """Get countries list latest updated."""
        url = "https://api.worldbank.org/v2/countries?per_page=5000"  # 目前的国家与地区数目为297个，远小于5000
        content = self.crawler.fetch_data(url)  # 获取内容为XML格式

        # 解析XML内容
        root = ET.fromstring(content)
        print(root)

        return
