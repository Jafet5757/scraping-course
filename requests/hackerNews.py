import requests
from bs4 import BeautifulSoup

# cambiamos el user-agent para que no nos bloquee la web
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3'
}

url = 'https://news.ycombinator.com/'

# Realizamos la petición a la web
response = requests.get(url, headers=headers)

# si obtenemos una respuesta correcta
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'lxml')

    # obtenemos las noticias
    news = soup.find_all('tr', class_="athing")

    for new in news:
        title = new.find('span', class_='titleline').text
        # obtenemor el url de la etiqueta a
        url = new.find('span', class_='titleline').find('a')["href"]
        # obtenemos la metadata del elemento hermano
        metadata = new.find_next_sibling('tr')

        score = 0
        comentarios = ''

        try:
            score = metadata.find('span', class_='score').text
            score = score.replace('points', '').strip()
            score = int(score)

            comentarios = metadata.find('span', attrs={'class': 'subline'}).text
            comentarios = comentarios.split('|')[-1].strip()
        except:
            score = 0
            comentarios = ''

        print(title)
        print(url)
        print(score)
        print(comentarios)
        print('-------------------')