from crawler import Crawler
from config import Config

import xml.etree.ElementTree as ET
import json
import os


class FieldManager:
    """Used for managing the retrieval and searching of options within a field."""

    def __init__(self) -> None:
        self._dict = {}
        self.search_idx = {}
        self.crawler = Crawler()

    def search(self, keyword):
        """Search for keyword in the dict."""
        return self.search_idx[keyword]

    def get_search_idx(self):
        """Get search index."""
        for k, v in self._dict.items():
            self.search_idx[v["name"]] = k

    def get_drop_down_list(self):
        """Get drop down list for the field."""
        return [v["name"] for k, v in self._dict.items()]


class CountryFieldManager(FieldManager):
    """Used for managing the country name list."""

    def __init__(self) -> None:
        super().__init__()
        self.get_countries_list()
        self.get_search_idx()

    def get_countries_list(self):
        if os.path.exists(Config.COUNTRIES_LIST_PATH):
            # if the country list file already exists, read it directly
            self._dict = json.load(open(Config.COUNTRIES_LIST_PATH, "r"))
            print("Countries list loaded from local cached file.")
            print("Countries list length: ", len(self._dict))
        else:
            # if the country list file does not exist, get it online
            self._dict = self.get_countries_list_online()
        return self._dict

    def get_countries_list_online(self):
        """Get countries list latest updated."""
        url = "https://api.worldbank.org/v2/countries?per_page=5000"  # the total number of countries and regions is 297, far less than 5000
        content = self.crawler.fetch_data(url)  # get content in XML format
        # remove illegal characters before XML content
        content = content[content.find("<"):]

        # parse XML content to get country info
        root = ET.fromstring(content)
        for country in root:
            country_id = country.attrib["id"]
            iso2Code = country[0].text
            country_name = country[1].text
            # print(country_id, iso2Code, country_name)

            # save country info to dict
            self._dict[country_id] = {
                "iso2Code": iso2Code, "name": country_name}

        # save country info to json file
        os.makedirs(Config.TMP_PATH, exist_ok=True)
        json.dump(self._dict, open(Config.COUNTRIES_LIST_PATH, "w"))
        return self._dict


class IndicatorFieldManager(FieldManager):
    """Used for managing the indicator name list."""

    def __init__(self) -> None:
        super().__init__()
        self.get_indicators_list()
        self.get_search_idx()

    def get_indicators_list(self):
        # GDP
        self._dict["NY.GDP.MKTP.CN"] = {
            "name": "GDP (current Local Currency Units)"}
        self._dict["NY.GDP.MKTP.CD"] = {"name": "GDP (current US$)"}
        self._dict["NY.GDP.MKTP.KN"] = {
            "name": "GDP (constant Local Currency Units)"}
        self._dict["NY.GDP.MKTP.KD"] = {"name": "GDP (constant 2015 US$)"}

        # GDP per capita
        self._dict["NY.GDP.PCAP.CN"] = {"name": "GDP per capita (current LCU)"}
        self._dict["NY.GDP.PCAP.CD"] = {"name": "GDP per capita (current US$)"}
        self._dict["NY.GDP.PCAP.KN"] = {
            "name": "GDP per capita (constant LCU)"}
        self._dict["NY.GDP.PCAP.KD"] = {
            "name": "GDP per capita (constant 2015 US$)"}
        return self._dict
