from wb_url_manager import WbUrlManager
from db_field_manager import CountryFieldManager


class Tester:
    def __init__(self) -> None:
        self.wb_url_manager = WbUrlManager()
        self.country_field_manager = CountryFieldManager()


    def test_get_countries_list(self):
        countries_list = self.country_field_manager.get_countries_list_online()
        print(countries_list)



if __name__ == "__main__":
    tester = Tester()
    tester.test_get_countries_list()
    