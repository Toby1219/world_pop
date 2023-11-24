from bs4 import BeautifulSoup
import requests
import pandas as pd
from fake_useragent import UserAgent
from others.mysqlite3 import SQlite
import json
import os


def get_request(url):
    ua = UserAgent()
    header = {"headers": ua.random}
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            print(response.status_code)
        else:
            print(re.status_code)
    except Exception as e:
        print(e)
        pass
    return response


def parse_html(response):
    soup = BeautifulSoup(response.content, 'html5lib')
    table = soup.find('table', {'id': "example2"}).find('tbody').find_all('tr')

    result = []
    for data in table:
        name_country = data.select('td')[1].a.text
        population = data.select('td')[2].text
        yearly_change = data.select('td')[3].text
        next_change = data.select('td')[4].text
        density = data.select('td')[5].text
        land_area = data.select('td')[6].text
        migrant = data.select('td')[7].text
        fer_rate = data.select('td')[8].text
        med_age = data.select('td')[9].text
        ubarn_pop = data.select('td')[10].text
        word_share = data.select('td')[11].text

        data = {
            'Country': name_country,
            'Population': population,
            'Yearly Change': yearly_change,
            'Next Change': next_change,
            'Density': density,
            'Land Area': land_area,
            'Migrant': migrant,
            'Fertility': fer_rate,
            'Median Age': med_age,
            'Ubarn Population': ubarn_pop,
            'Word Share': word_share
        }
        data2 = (name_country, population, yearly_change, next_change, density, land_area, migrant,
                 fer_rate, med_age, ubarn_pop, word_share)
        sql_writer(data2)
        result.append(data)
    print("Done Scrapeing.......")
    return result


def writer_(data):
    path = 'data'
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        pass
    df = pd.DataFrame(data)
    df.to_csv('data/world.csv', index=False)
    df.to_excel('data/world.xlsx', index=False)
    with open('data/world.json', 'w') as file:
        json.dump(data, file, indent=2)


def sql_writer(data):
    path = 'data'
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        pass
    sq = SQlite('data/world.db', 'world')
    sq.create_table('Country TEXT', 'Population INT', 'Yearly Change INT', 'Next Change INT',
                    'Density INT', 'Land Area INT', 'Migrant INT', 'Fertility INT', 'Median Age INT',
                    'Ubarn Population INT', 'Word Share INT')
    sq.insert_table(data)
    sq.view_all('rowid', '*', all_=False)


def main():
    url = 'https://www.worldometers.info/world-population/population-by-country/'
    response = get_request(url)
    data = parse_html(response)
    writer_(data)


if __name__ == '__main__':
    main()

