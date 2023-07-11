import requests
from bs4 import BeautifulSoup
import re

# Base-URL
base_url = 'https://www.livsmedelsverket.se/livsmedel-och-innehall/tillsatser-e-nummer/sok-e-nummer/'

response = requests.get(base_url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=re.compile(r'/sok-e-nummer/.*'))

    
    for link in links:
        url = base_url + link['href']

        
        response = requests.get(url)
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.find('h1').text.strip()
            print(title)
        else:
            print('Misslyckades att hämta webbsidan. Statuskod:', response.status_code)
else:
    print('Misslyckades att hämta bas-URL:n. Statuskod:', response.status_code)
