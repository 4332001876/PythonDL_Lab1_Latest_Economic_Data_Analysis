from wb_url_manager import WbUrlManager
from db_field_manager import CountryListManager


class Tester:
    def __init__(self) -> None:
        self.wb_url_manager = WbUrlManager()


    def test_get_countries_list(self):
        countries_list = self.wb_url_manager.get_countries_list()
        print(countries_list)
        return



if __name__ == "__main__":
    tester = Tester()
    tester.test_get_countries_list()
    