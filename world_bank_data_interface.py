from db_field_manager import CountryFieldManager, IndicatorFieldManager
from crawler import Crawler

import xml.etree.ElementTree as ET
import pandas as pd

BASE_URL = "https://api.worldbank.org/v2"
COUNTRIES_URL_PART = "/countries"
INDICATOR_URL_PART = "/indicators"


class WbDataInterface:
    """Used for fetching GDP data from world bank api."""

    def __init__(self) -> None:
        self.country_field_manager = CountryFieldManager()
        self.indicator_field_manager = IndicatorFieldManager()
        self.crawler = Crawler()

    def _get_url(self, country_name, indicator_name):
        """Get world bank api url for the specific country and indicator."""
        url = BASE_URL + \
            COUNTRIES_URL_PART + "/" + self.country_field_manager.search(country_name) + \
            INDICATOR_URL_PART + "/" + \
            self.indicator_field_manager.search(indicator_name)
        return url

    def get_data(self, country_name, indicator_name) -> pd.DataFrame:
        """Get data from world bank api by country name and indicator name."""
        # fetch xml
        url = self._get_url(country_name, indicator_name)
        xml = self.crawler.fetch_data(url)
        xml = xml[xml.find("<"):]

        # parse xml to GDP data
        root = ET.fromstring(xml)
        df_rows = []
        for data in root:
            data_year = int(data[3].text)
            if data[4].text is not None:
                data_value = float(data[4].text)
                # print(data_year, data_value)
                df_rows.append(
                    {"Year": data_year, "GDP": data_value})
        df = pd.DataFrame(df_rows)
        if df.shape[0] > 0:
            df = df.sort_values(by=["Year"], ascending=False)
        return df
