from world_bank_data_interface import WbDataInterface
from server import Server
from db_field_manager import CountryFieldManager


class Tester:
    def __init__(self) -> None:
        self.server = Server()
        self.country_field_manager = CountryFieldManager()
        self.wb_data_interface = WbDataInterface()


    def test_get_countries_list(self):
        countries_list = self.country_field_manager.get_countries_list_online()
        print(countries_list)

    def get_example_data(self):
        return self.wb_data_interface.get_data("China", "GDP (current Local Currency Units)")

if __name__ == "__main__":
    tester = Tester()
    tester.get_example_data()
    