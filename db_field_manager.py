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
        self._dict = self.get_countries_list()

    def get_countries_list(self):
        if os.path.exists(Config.COUNTRIES_LIST_PATH):
            # 如果已经存在国家列表文件，则直接读取
            self._dict = json.load(open(Config.COUNTRIES_LIST_PATH, "r"))
            print("Countries list loaded from cached local file.")
            print("Countries list length: ", len(self._dict))
        else:
            # 如果不存在国家列表文件，则在线获取
            self._dict = self.get_countries_list_online()
        return self._dict

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


class IndicatorFieldManager(FieldManager):
    def __init__(self) -> None:
        super().__init__()
        self._dict = self.get_indicators_list()

    def get_indicators_list(self):
        # GDP总量
        self._dict["NY.GDP.MKTP.CN"] = {
            "name": "GDP (current Local Currency Units)"}
        self._dict["NY.GDP.MKTP.CD"] = {"name": "GDP (current US$)"}
        self._dict["NY.GDP.MKTP.KN"] = {
            "name": "GDP (constant Local Currency Units)"}
        self._dict["NY.GDP.MKTP.KD"] = {"name": "GDP (constant 2015 US$)"}

        # 人均GDP
        self._dict["NY.GDP.PCAP.CN"] = {"name": "GDP per capita (current LCU)"}
        self._dict["NY.GDP.PCAP.CD"] = {"name": "GDP per capita (current US$)"}
        self._dict["NY.GDP.PCAP.KN"] = {
            "name": "GDP per capita (constant LCU)"}
        self._dict["NY.GDP.PCAP.KD"] = {
            "name": "GDP per capita (constant 2015 US$)"}
