import requests
import bs4 as bs


url = 'https://country-code.cl/'

print(' * Downloading website content...')
r = requests.get(url)

soup = bs.BeautifulSoup(r.content, 'html.parser')

table = soup.find_all('table')[6]
body = table.find('tbody')
trs = body.find_all('tr')

countries : list[str] = []
codes : list[str] = []

print(' * Parsing content...')
for tr in trs:
    tds = tr.find_all('td')
    
    country = tds[2].find_all('span')[0].text
    countries.append(country.replace('-', '_').upper())
    codes.append(tds[3].text.replace('\n', '').replace(' ', ''))


print('\n Content:')
for country, code in zip(countries, codes):
    print(f'{country} = "{code}"')
