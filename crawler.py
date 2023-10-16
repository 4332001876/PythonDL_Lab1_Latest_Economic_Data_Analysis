from config import Config
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


class Crawler:
    def __init__(self) -> None:
        pass

    def fetch_data(self, url):
        # sleep for n second to avoid being blocked
        time.sleep(Config.SLEEP_TIME)
        headers = {"User-Agent": Config.USER_AGENT, 'Cookie': Config.COOKIE}
        response = requests.get(url, headers=headers)
        return response.text
