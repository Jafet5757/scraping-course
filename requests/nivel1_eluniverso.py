from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class Noticia(Item):
  titular = Field()
  descripcion = Field()


class ElUniversoSpider(Spider):
  name = "MiSegundoSpider"
  custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
      (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 \
      Safari/537.36'
  }

  start_urls = ['https://www.eluniverso.com/deportes/']

  def parse(self, response):
    """ sel  = Selector(response)
    cards = sel.xpath('//li[@class="relative "]')
    for card in cards:
      item = ItemLoader(Noticia(), card)
      item.add_xpath('titular', './/h2/a/text()')
      item.add_xpath('descripcion', './/p/text()')

      yield item.load_item() """
    soup = BeautifulSoup(response.body)
    cards = soup.find_all('li', class_='relative')

    for card in cards:
      titular = card.find('h2').text
      description = card.find('p')

      if description == None:
        description = 'No hay descripción'
      else:
        description = description.text

      item = ItemLoader(Noticia(), response.body)
      item.add_value('titular', titular)
      item.add_value('descripcion', description)
    
      yield item.load_item()