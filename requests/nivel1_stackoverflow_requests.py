import requests
from bs4 import BeautifulSoup


# cambiamos el user-agent para que no nos bloquee la web
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'
}

url = 'https://stackoverflow.com/questions'

# Realizamos la petición a la web
response = requests.get(url, headers=headers)

# parseamos la respuesta
soup = BeautifulSoup(response.text)

#buscamos por id
questions = soup.find(id='questions')

# obtenemos todos los elementos de la clase question-summary
question_summary = questions.find_all('div',class_='s-post-summary')

for question in question_summary:
  text = question.find('h3').find('a').text
  description = question.find('div', class_='s-post-summary--content-excerpt').text
  print(text)
  print(description.replace('\n','').strip())
  print('-------------------')