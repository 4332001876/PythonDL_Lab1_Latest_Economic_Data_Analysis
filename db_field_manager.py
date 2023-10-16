from crawler import Crawler
from config import Config

import xml.etree.ElementTree as ET
import json
import os


class FieldManager:
    def __init__(self) -> None:
        self._dict = {}
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
        content = content[content.find("<"):]  # 去除XML内容前的非法字符

        # 解析XML内容
        root = ET.fromstring(content)
        for country in root:
            country_id = country.attrib["id"]
            iso2Code = country[0].text
            country_name = country[1].text
            # print(country_id, iso2Code, country_name)

            # 将国家信息存入dict
            self._dict[country_id] = {
                "iso2Code": iso2Code, "name": country_name}

        # 将dict存入json文件
        os.makedirs(Config.TMP_PATH, exist_ok=True)
        json.dump(self._dict, open(Config.COUNTRIES_LIST_PATH, "w"))
        return self._dict
