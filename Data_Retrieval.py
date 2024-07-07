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


def scrape_table(part):
    try:
        response = requests.get(URL)
        print(response)
        logging.info(f'Scraping {part} table')
        soup = BeautifulSoup(response.text, 'html.parser')
        parting_section = soup.find('section', attrs={'id': f'{part}'})
        logging.info(f'Scraping {part} table section')

        parting_table = parting_section.find('table')
        parting_body = parting_table.find_all('tr')
        station_names = []
        logging.info(f'Scraping {part} table name')

        for i in range(1, len(parting_body)):
            station_names.append(station_text(parting_body[i]))

        logging.info("Names generated")

        return station_names

    except Exception as e:
        logging.error(f'Error fetching {e}')

def convert_to_json(line):
    try:
        logging.info(f'Converting {line}')
        lines = scrape_table(line)
        convert = {line : lines}

        with open(f'{line}.json', 'w') as outfile:
            json.dump(convert, outfile)

        logging.info(f'Finished converting {line}')

    except Exception as e:
        logging.error(f'Error converting: {e}')

def convert_all(stations_lines):
    try:
        logging.info(f'Converting all lines')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(convert_to_json, stations_lines)
        logging.info(f'Concurrency achieved.')

    except Exception as e:
        logging.error(f'Error converting: {e}')

def get_ids():
    try:
        logging.info(f'Getting ids')
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        sections = soup.find_all('section')

        ids = [section.get('id') for section in sections]

        logging.info(f'Done fetching ids')

        return ids

    except Exception as e:
        logging.error(f'Error fetching id names {e}')

if __name__ == '__main__':

    station_names = get_ids()
    print(station_names)

    convert_all(station_names)
