import numpy as np
import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
import json
logging.basicConfig(
    filename='scrape.log',
    filemode='a',
    format= '%(asctime)s - %(levelname)s - %(message)s',
    level= logging.INFO
)
URL = 'https://en.wikipedia.org/wiki/Pink_Line_(Delhi_Metro)'

def pinkCoord():
    try:
        respo = requests.get(URL)
        print(respo)
        logging.info(f'Scrapping in progress')

        soup = BeautifulSoup(respo.text, 'html.parser')
        table_body = soup.find('table', attrs={'class': 'wikitable'})
        table_links = table_body.find_all('b')

        alinks = [table_links[i].find('a') for i in range(0, len(table_links))]
        alinks = [i for i in alinks if i is not None]

        links = [alinks[i].get('href') for i in range(0, len(alinks))]
        links = links[9::1]

        # index 21, 22, 23, 31 ,32 ,33 will give error
        links.pop(21)
        links.pop(21)
        links.pop(21)
        links.pop(28)
        links.pop(28)
        links.pop(28)


        logging.info(f'Successfully Scrapped the links to pages')

        dii = []

        for i in range(0, len(links)):
            stnURL = f'https://en.wikipedia.org{links[i]}'
            respw = requests.get(stnURL)
            logging.info(f'Scrapping {stnURL}')

            print(respw)
            soup = BeautifulSoup(respw.text, 'html.parser')
            spans = soup.find('span', class_='plainlinks nourlexpansion')

            spans_anchor = spans.find('a')
            link_coord = spans_anchor.get('href')

            resps = requests.get(link_coord)
            print(f'geohack response : {resps}')
            sooup = BeautifulSoup(resps.text, 'html.parser')

            # geo_span = sooup.find('span', class_='geo')

            latit = float(sooup.find('span', class_='latitude').text.strip())
            longit = float(sooup.find('span', class_='longitude').text.strip())
            logging.info(f'Successfully Scrapped longitude and latitude of {stnURL}')

            dii.append([latit, longit])
        return dii

    except Exception as e:
        logging.error(f'Error fetching {e}')

def magcoordinates(magURL):
    try:
        respo = requests.get(magURL)
        print(respo)
        logging.info(f'Scrapping in progress')

        soup = BeautifulSoup(respo.text, 'html.parser')
        table_body = soup.find_all('table', attrs={'class': 'wikitable'})
        table_body = table_body[1]

        table_links = table_body.find_all('b')

        alinks = [table_links[i].find('a') for i in range(0, len(table_links))]
        alinks = [i for i in alinks if i is not None]
        links = [alinks[i].get('href') for i in range(0, len(alinks))]

        links = links[22:]
        links.pop(6)
        links.pop(2)

        links.pop(3)
        links.pop(3)
        links.pop(7)

        logging.info(f'Successfully Scrapped the links to pages')

        dii = []

        for i in range(0, len(links)):
            stnURL = f'https://en.wikipedia.org{links[i]}'
            respw = requests.get(stnURL)

            logging.info(f'Scrapping {stnURL}')

            print(respw)
            soup = BeautifulSoup(respw.text,'html.parser')
            spans = soup.find('span', class_='plainlinks nourlexpansion')

            spans_anchor = spans.find('a')
            link_coord = spans_anchor.get('href')

            resps = requests.get(link_coord)
            print(f'geohack response : {resps}')
            sooup = BeautifulSoup(resps.text, 'html.parser')

            # geo_span = sooup.find('span', class_='geo')

            latit = float(sooup.find('span', class_='latitude').text.strip())
            longit = float(sooup.find('span', class_='longitude').text.strip())
            logging.info(f'Successfully Scrapped longitude and latitude of {stnURL}')

            dii.append([latit,longit])
        return dii

    except Exception as e:
        logging.error(f'Error fetching {e}')

def greenCoordinates(gURL):
    try:
        respo = requests.get(gURL)
        print(respo)
        logging.info(f'Scrapping in progress')

        soup = BeautifulSoup(respo.text, 'html.parser')
        table_body = soup.find_all('table', attrs={'class': 'wikitable'})
        # table_links = table_body[0].find_all('b')

        table_links = table_body[1].find_all('b')

        alinks = [table_links[i].find('a') for i in range(0, len(table_links))]
        alinks = [i for i in alinks if i is not None]
        links = [alinks[i].get('href') for i in range(0, len(alinks))]

        # links = links[6:]
        # links.pop(5)
        # links[9] = '/wiki/Udyog_Nagar_metro_station'
        #
        # links.pop(13)
        # links.insert(15, '/wiki/Mundka_Industrial_Area_metro_station')

        links.pop(2)  # For Branch
        print(links)
        logging.info(f'Successfully Scrapped the links to pages')

        dii = []

        for i in range(0, len(links)):
            stnURL = f'https://en.wikipedia.org{links[i]}'
            respw = requests.get(stnURL)
            logging.info(f'Scrapping {stnURL}')

            print(respw)
            soup = BeautifulSoup(respw.text,'html.parser')
            spans = soup.find('span', class_='plainlinks nourlexpansion')

            spans_anchor = spans.find('a')
            link_coord = spans_anchor.get('href')



            resps = requests.get(link_coord)
            print(f'geohack response : {resps}')
            sooup = BeautifulSoup(resps.text, 'html.parser')

            # geo_span = sooup.find('span', class_='geo')

            latit = float(sooup.find('span', class_='latitude').text.strip())
            longit = float(sooup.find('span', class_='longitude').text.strip())
            logging.info(f'Successfully Scrapped longitude and latitude of {stnURL}')

            dii.append([latit,longit])
        return dii

    except Exception as e:
        logging.error(f'Error fetching {e}')


def main():
    try:


        # pcoord = pinkCoord()
        # print(len(pcoord))

        # magCoord = magcoordinates('https://en.wikipedia.org/wiki/Magenta_Line_(Delhi_Metro)')
        # print(magCoord)
        # print(len(magCoord))

        gCoord = greenCoordinates('https://en.wikipedia.org/wiki/Green_Line_(Delhi_Metro)')
        '''
        Manual updation done for Airport-Express Line
        # Remove index 1 and after which remove index 5 for airport express
        # coord.pop(1)
        # coord.pop(5)  
        '''
        f = open('GreenLine.json')
        dat = json.load(f)

        dat = dat['GreenLine']
        cordDict = {}
        '''
        Below is the manual updation is done for Green Line's coordinates retrieval
        dat[2] = 'Punjabi Bagh (East)'
        dat.insert(3, 'Punjabi Bagh (West)')
        '''
        '''
         Manual updation for Magenta Line
        # cordDict.update({dat[0] : magCoord[0]})
        # cordDict.update({dat[1]: magCoord[1]})
        # cordDict.update({dat[2]: [28.602526, 77.082532]})
        
        # cordDict.update({dat[3]: magCoord[2]})
        # cordDict.update({dat[4]: [28.577492, 77.111346]})
        # cordDict.update({dat[5] : [28.565293, 77.122411]})
    
        # cordDict.update({dat[6] : magCoord[3]})
        # cordDict.update({dat[7] : magCoord[4]})
        # cordDict.update({dat[8] : magCoord[5]})
    
        # cordDict.update({dat[9] : magCoord[6]})
        # cordDict.update({dat[10] : [28.548068, 77.193618]})
        '''

        i = 0
        j = 0

        while i < len(dat) and j < len(gCoord):
            cordDict.update({dat[i]: gCoord[j]})
            i += 1
            j += 1

        cordDict = {'GreenLine-Branch': cordDict}
        with open('greenSecondBranch.json', 'w') as fil : json.dump(cordDict,fil)
    except Exception as err:
        logging.error(f'Error in main process : {err}')


if __name__ == "__main__":
    main()