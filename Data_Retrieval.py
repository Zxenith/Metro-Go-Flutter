import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import concurrent.futures
import json
import logging

URL = "https://delhimetrorail.info/delhi-metro-stations"

logging.basicConfig(
    filename='data_py.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def station_text(tr):
    station_name_distance = tr.find('td', class_= 'left')
    station_name = station_name_distance.find('a').text.strip()
    return station_name
def scrape_table(part, URL):
    try:
        response = requests.get(URL)
        print(response)
        logging.info(f'Scraping {part} table')
        soup = BeautifulSoup(response.text, 'html.parser')
        parting_section = soup.find('section', attrs={'id': f'{part}'})

        parting_table = parting_section.find('table')
        parting_body = parting_table.find_all('tr')
        station_names = []

        for i in range(1, len(parting_body)):
            station_names.append(station_text(parting_body[i]))

        return station_names

    except Exception as e:
        logging.error(f'Error fetching {e}')


scrape_table('RedLine', URL)

