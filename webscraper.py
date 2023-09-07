import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import os

db_filename = "e_numbers.db"

# get href for all e-numbers
base_url = 'https://www.livsmedelsverket.se/livsmedel-och-innehall/tillsatser-e-nummer/sok-e-nummer'
response = requests.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")
links = soup.find_all("a", class_="name")
hrefs = [link["href"] for link in links]
e_nummer = []
for href in hrefs:
    e_nummer.append(href.split("sok-e-nummer")[1])

#Add all hrefs to the base_url
urls = []
for value in e_nummer:
    urls.append('https://www.livsmedelsverket.se/livsmedel-och-innehall/tillsatser-e-nummer/sok-e-nummer'+ value)

dfs =[]

for end in urls:
    res = requests.get(end)
    if res.status_code == 200:
        data_soup = BeautifulSoup(res.content, "html.parser")
        title = data_soup.find('h1').text.strip()
        name = title.split('-', 1)[1]
        
        body = data_soup.find("div", class_= "enumber-details")
        if body:
            information_dict = {}
            information_dict['titles'] = name
            
            elements = body.find_all(['p', 'h4'])
            current_h4 = None

            for element in elements:
                if element.name == 'h4':
                    current_h4 = element.text.strip()
                elif element.name == 'p' and current_h4:
                    information_dict[current_h4] = element.text.strip()
                
            df = pd.DataFrame([information_dict])
            dfs.append(df)
        else:
          print("kunde inte hämta body.")
    else:
        print("Kunde inte hämta titlar")

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), db_filename)

result_df = pd.concat(dfs, ignore_index=True)

conn = sqlite3.connect('e_numbers.db')
result_df.to_sql('E_numbers', conn, if_exists='replace', index=False)
conn.close()