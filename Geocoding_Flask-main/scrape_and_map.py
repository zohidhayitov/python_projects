from urllib.request import urlopen
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
from unidecode import unidecode
import pandas as pd
import numpy as np


geolocator = Nominatim(user_agent='flask_geo_app')
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def generate_euro_capitals():
    url = 'https://en.wikipedia.org/wiki/Template:Capital_cities_of_European_Union_member_states'
    page = urlopen(url)
    html = page.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    tbodies = soup.find_all('tbody')
    countries_and_capitals = []
    for i, tbody in enumerate(tbodies):
        if i == 0:
            pass
        else:
            tds = tbody.find('td')
            ahrefs = tds.find_all('a')
            country = ahrefs[0]['title']
            capital = ahrefs[1]['title']
            countries_and_capitals.append((country, capital))

    m = folium.Map()
    for loc_tuple in countries_and_capitals:
        country, capital = loc_tuple[0], loc_tuple[1]
        location = {'country': country, 'city': capital}
        coordinates = geocode(location)
        lat, lon = coordinates.point.latitude, coordinates.point.longitude
        tooltip = f'{country}: {capital}'
        folium.Marker([lat, lon], tooltip=tooltip).add_to(m)
    
    m.save('templates/european_capitals.html')

class CountryData:
    def __init__(self, df_path):
        dataframe = pd.DataFrame(
            data={'country': [], 'gdp_per_capita': [], 'capital': [], 'latitude': [], 'longitude': []},
            index=None
        )
        self.df_path = df_path
        self.dataframe = pd.DataFrame(dataframe)
        self.dataframe.to_csv(self.df_path)

    def get_current_df(self):
        return pd.read_csv(self.df_path)

    def set_new_df(self, new_df):
        new_df.to_csv(self.df_path)

    def scrape_gdp(self):
        url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita'
        page = urlopen(url)
        html = page.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        trs = soup.find_all('tr')
        countries = []
        gdp_per_capita = []
        for tr in trs:
            tds = tr.find_all('td')
            for j, td in enumerate(tds):
                # Scrape Countries
                if td.get('scope'):
                    country = td.find('a')['title']
                    countries.append(country)
                # Scrape GDP
                elif len(countries) > 0 and len(gdp_per_capita) < len(countries):
                    if '2019' == td.contents[0]:
                        gdp = tds[j-1].contents[0]
                        gdp_per_capita.append(gdp)
                        break
                    elif td == tds[-1]:
                        gdp_per_capita.append(np.nan)
                        break
        df = CountryData.get_current_df(self)
        df.country, df.gdp_per_capita = pd.Series(countries), pd.Series(gdp_per_capita)
        CountryData.set_new_df(self, df)

    @staticmethod
    def scrape_capitals():
        url = 'https://www.worlddata.info/capital-cities.php'
        page = urlopen(url)
        html = page.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        rows = soup.find_all('tr')

        countries, capitals = [], []
        for row in rows:
            table_data = row.find_all('td')
            try:
                country = table_data[0].find('a').contents[0]
                capital = table_data[1].contents[0]
                countries.append(country)
                capitals.append(capital)
            except:
                pass
        return countries, capitals

    def match_country_capital(self):
        df = CountryData.get_current_df(self)
        df['country'] = df['country'].apply(lambda x: unidecode(x))
        df.loc[df['country']=='Macau', ['country']] = 'Macao'
        df.loc[df['country']=='Czech Republic', ['country']] = 'Czechia'
        df.loc[df['country']=='Georgia (country)', ['country']] = 'Georgia'

        countries, capitals = CountryData.scrape_capitals()

        for country, capital in zip(countries, capitals):
            if any(country in c for c in df.country.to_list()):
                index = df.index[df['country'].str.contains(country)]
                df.loc[index, 'capital'] = capital
        CountryData.set_new_df(self, df)

    def geocode_coordinates(self):
        df = CountryData.get_current_df(self)
        for country, capital in zip(df.country, df.capital):
            location = {'country': country, 'city': capital}
            try:
                coordinates = geocode(location)
                lat, lon = coordinates.point.latitude, coordinates.point.longitude
                df.loc[df.country == country, 'latitude'] = lat
                df.loc[df.country == country, 'longitude'] = lon
            except:
                coordinates = geocode(country)
                lat, lon = coordinates.point.latitude, coordinates.point.longitude
                df.loc[df.country == country, 'latitude'] = lat
                df.loc[df.country == country, 'longitude'] = lon
        CountryData.set_new_df(self, df)

    def geomap_country_gdp(self):
        df = CountryData.get_current_df(self)
        m = folium.Map()
        for country, capital, gdp in zip(df.country, df.capital, df.gdp_per_capita):
            lat, lon = df.loc[df.country == country, 'latitude'], df.loc[df.country== country, 'longitude']
            tooltip = f'{country}, {capital}: ${gdp}'
            folium.Marker([lat, lon], tooltip=tooltip).add_to(m)
        m.save('templates/country_cap_gdp_per_capita.html')

    def gen_geomap_country_gdp(self):
        CountryData.scrape_gdp(self)
        CountryData.match_country_capital(self)     # calls scrape_capitals()
        CountryData.geocode_coordinates(self)
        CountryData.geomap_country_gdp(self)




def create_country_df():
    d = {
        'country': [],
        'gdp_per_capita': [],
        'capital': [],
        'latitude': [],
        'longitude': [],
        }
    df = pd.DataFrame(data=d, index=None)
    df.to_csv('country_db.csv')

def scrape_country_gdp():
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita'
    page = urlopen(url)
    html = page.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    trs = soup.find_all('tr')
    countries = []
    gdp_per_capita = []
    for tr in trs:
        tds = tr.find_all('td')
        for j, td in enumerate(tds):
            # Scrape Countries
            if td.get('scope'):
                country = td.find('a')['title']
                countries.append(country)
            # Scrape GDP
            elif len(countries) > 0 and len(gdp_per_capita) < len(countries):
                if '2019' == td.contents[0]:
                    gdp = tds[j-1].contents[0]
                    gdp_per_capita.append(gdp)
                    break
                elif td == tds[-1]:
                    gdp_per_capita.append(np.nan)
                    break
    df = pd.read_csv('country_db.csv', index_col=0)
    df.country, df.gdp_per_capita = pd.Series(countries), pd.Series(gdp_per_capita)
    df.to_csv('country_db.csv')

def scrape_capitals():
    url = 'https://www.worlddata.info/capital-cities.php'
    page = urlopen(url)
    html = page.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    rows = soup.find_all('tr')

    countries, capitals = [], []
    for row in rows:
        table_data = row.find_all('td')
        try:
            country = table_data[0].find('a').contents[0]
            capital = table_data[1].contents[0]
            countries.append(country)
            capitals.append(capital)
        except:
            pass
    return countries, capitals

def match_country_capital():
    df = pd.read_csv('country_db.csv', index_col=0)
    df['country'] = df['country'].apply(lambda x: unidecode(x))
    df.loc[df['country']=='Macau', ['country']] = 'Macao'
    df.loc[df['country']=='Czech Republic', ['country']] = 'Czechia'
    df.loc[df['country']=='Georgia (country)', ['country']] = 'Georgia'

    countries, capitals = scrape_capitals()

    for country, capital in zip(countries, capitals):
        if any(country in c for c in df.country.to_list()):
            index = df.index[df['country'].str.contains(country)]
            df.loc[index, 'capital'] = capital
    df.to_csv('country_db.csv')

def geocode_coordinates():
    df = pd.read_csv('country_db.csv')
    for country, capital in zip(df.country, df.capital):
        location = {'country': country, 'city': capital}
        try:
            coordinates = geocode(location)
            lat, lon = coordinates.point.latitude, coordinates.point.longitude
            df.loc[df.country == country, 'latitude'] = lat
            df.loc[df.country == country, 'longitude'] = lon
        except:
            coordinates = geocode(country)
            lat, lon = coordinates.point.latitude, coordinates.point.longitude
            df.loc[df.country == country, 'latitude'] = lat
            df.loc[df.country == country, 'longitude'] = lon
    df.to_csv('country_db.csv')

def geomap_country_gdp():
    df = pd.read_csv('country_db.csv')
    m = folium.Map()
    for country, capital, gdp in zip(df.country, df.capital, df.gdp_per_capita):
        lat, lon = df.loc[df.country == country, 'latitude'], df.loc[df.country== country, 'longitude']
        tooltip = f'{country}, {capital}: ${gdp}'
        folium.Marker([lat, lon], tooltip=tooltip).add_to(m)
    m.save('templates/country_cap_gdp_per_capita.html')

def gen_geomap_country_gdp():
    create_country_df()
    scrape_country_gdp()
    match_country_capital()     # calls scrape_capitals()
    geocode_coordinates()
    geomap_country_gdp()

