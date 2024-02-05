import requests
from lxml import html
import json

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'
}

respuesta = requests.get('https://www.gob.pe/busquedas?term=recibo&institucion=&topic_id=&contenido=&sort_by=none', headers=headers)

respuesta.encoding = 'UTF-8'

parser = html.fromstring(respuesta.text)

datos = parser.xpath('//script[contains(text(), "window.initialData")]')[0].text_content()

indice_inicial = datos.find('{')
datos = datos[indice_inicial:]

# lo convertimos a json
objeto = json.loads(datos)
resultados = objeto["data"]["attributes"]["results"]

for r in resultados:
  print(r['content'])