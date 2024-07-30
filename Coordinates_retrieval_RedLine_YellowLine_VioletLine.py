import numpy as np
import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
import json

logging.basicConfig(
    filename='DelhiMetroScrapeLogs.log',
    filemode='a',
    format= '%(asctime)s - %(levelname)s - %(message)s',
    level= logging.INFO
)

URL = 'https://en.wikipedia.org/wiki/Delhi_Metro'

def lines():

    try:
        respo = requests.get(URL)
        print(respo)
        logging.info(f'Scrapping in progress')

        soup = BeautifulSoup(respo.text, 'html.parser')
        table_body = soup.find('table', attrs={'class': 'infobox'})
        table_links = table_body.find('div', attrs={'class': 'plainlist'})

        line_anchors = table_links.find_all('a')
        line_links = [line_anchors[i].get('href') for i in range(0,len(line_anchors))]
        logging.info("Successfully scrapped links of lines")
        return line_links
    except Exception as e:
        logging.error(f'Error fetching {e}')


def stnLinks(baseURL):
    try:
        respo1 = requests.get(baseURL)
        print(respo1)
        soupy = BeautifulSoup(respo1.text, 'html.parser')

        logging.info(f'Scrapping {baseURL}')
        stn_table = soupy.find_all('table', class_='wikitable')
        stn_table = stn_table[1]

        stn_tr = stn_table.find_all('tr')
        stn_btag = [i.find('b') for i in stn_tr]
        stn_btag = [i for i in stn_btag if i is not None]
        logging.info(f'Scrapping of anchor tags in progress')

        stn_anchors = [i.find('a') for i in stn_btag]
        stn_anchors = [i for i in stn_anchors if i is not None]
        stn_links = [i.get('href') for i in stn_anchors]
        logging.info(f'Successfully scrapped station links')

        return stn_links
    except Exception as e:
        logging.error(f'Error fetching {e}')


def violetStnNames(baseURL):
    try:
        respo1 = requests.get(baseURL)
        print(respo1)
        soupy = BeautifulSoup(respo1.text, 'html.parser')

        logging.info(f'Scrapping {baseURL}')
        stn_table = soupy.find_all('table', class_='wikitable')
        stn_td = stn_table[1].find_all('td')

        stn_anc = [i.find('a') for i in stn_td]
        stn_anc = [i for i in stn_anc if i is not None]
        stn_links = [stn_anc[i].get('href') for i in range(0, len(stn_anc))]

        return stn_links

        # stn_td = stn_table.find_all('td', class_='RMr')
        # stn_anchors = [stn_td[i].find('a') for i in range(0, len(stn_td))]
        # stn_anchors = [i for i in stn_anchors if i is not None]
        # for i in stn_anchors:
        #     print(i)
        #
        # print(len(stn_anchors))

    except Exception as e:
        logging.error(f'Error fetching {e}')


def coordinates(stnURL):
    try:
        resp = requests.get(stnURL)
        print(resp)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')

            spans = soup.find('span', class_='plainlinks')
            spans_anchor = spans.find('a')
            link_coord = spans_anchor.get('href')

            resps = requests.get(link_coord)
            print(f'geohack response : {resps}')
            sooup = BeautifulSoup(resps.text, 'html.parser')

            latit = float(sooup.find('span', class_ = 'latitude').text.strip())
            longit = float(sooup.find('span', class_='longitude').text.strip())

            logging.info(f'Successfully Scrapped longitude and latitude of {stnURL}')
        return [latit, longit]

    except Exception as e:
        logging.error(f'Error fetching {e}')


if __name__ == "__main__":

    mLines = lines()
    # redStns = stnLinks(f'https://en.wikipedia.org{mLines[0]}')
    # yellowStns = stnLinks(f'https://en.wikipedia.org{mLines[1]}')
    # blueStns = stnLinks(f'https://en.wikipedia.org{mLines[2]}')
    # greenStns = stnLinks(f'https://en.wikipedia.org{mLines[3]}')
    vioStns = violetStnNames(f'https://en.wikipedia.org{mLines[4]}')
    # airpExp = stnLinks(f'https://en.wikipedia.org{mLines[5]}')
    # pinkStns = stnLinks(f'https://en.wikipedia.org{mLines[6]}')
    # magStns = stnLinks(f'https://en.wikipedia.org{mLines[7]}')
    # grayStns = stnLinks(f'https://en.wikipedia.org{mLines[8]}')
    # yellowStns[6] = '/wiki/Model_Town_metro_station,_Delhi'
    # for violet line, remove index 28 and 34

    coord = []
    for i in vioStns:
        bUrl = f'https://en.wikipedia.org{i}'
        loc = coordinates(bUrl)
        coord.append(loc)
    coord = [i for i in coord if i is not None]
    print(coord)
    coord.pop(28)
    coord.pop(33)

    # print(airpExp)
    # print(pinkStns)
    # print(magStns)
    # print(grayStns)
    # for i in range(0,len(vioStns)):
    #     bURl = f'https://en.wikipedia.org{[i]}'
    #     coord.append(coordinates(bURl))
    # coord = [i for i in coord if i is not None]
    #
    # for i in coord:
    #     print(i)

    f = open('VioletLine.json')
    ylwStn = json.load(f)

    ylwStn = ylwStn['VioletLine']
    ylwCoord = {}

    ylwCoord.update({ylwStn[0] : coord[0]})
    ylwCoord.update({ylwStn[1] : coord[1]})
    ylwCoord.update({ylwStn[2]: [28.6495714, 77.238016]})

    i = 3
    j = 2
    while i < len(ylwStn) and j < len(coord):
        ylwCoord.update({ylwStn[i]: coord[j]})
        i += 1
        j += 1
    redCoord = {'VioletLine':ylwCoord}
    with open('violet.json','w') as fi : json.dump(redCoord,fi)
