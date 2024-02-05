import requests # hace petitiones a la web
from lxml import html # para parsear el html

# cambiamos el user-agent para que no nos bloquee la web
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'
}

url = "https://www.wikipedia.org/"

# Realizamos la petición a la web
response = requests.get(url, headers=headers)

parser = html.fromstring(response.text)

# Obtenemos el id de la etiqueta que contiene el texto en inglés
ingles = parser.get_element_by_id("js-link-box-en")

print(ingles.text_content())

# Obtenemos el elemento usando Xpath
espanol = parser.xpath('//a[@id="js-link-box-es"]/strong/text()')

print(espanol[0])

# Obtenemos todos los idiomas
idiomas = parser.xpath("//div[contains(@class, 'central-featured-lang')]//strong/text()")

for idioma in idiomas:
    print(idioma)