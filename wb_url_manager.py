from db_field_manager import CountryFieldManager, IndicatorFieldManager

BASE_URL = "https://api.worldbank.org/v2"
COUNTRIES_URL_PART = "/countries"
INDICATOR_URL_PART = "/indicators"


class WbUrlManager:
    def __init__(self) -> None:
        self.country_field_manager = CountryFieldManager()
        self.indicator_field_manager = IndicatorFieldManager()

    def get_url(self, country_name, indicator_name):
        url = BASE_URL + \
            COUNTRIES_URL_PART + "/" + self.country_field_manager.search(country_name) + \
            INDICATOR_URL_PART + "/" + \
            self.indicator_field_manager.search(indicator_name)
        return url
