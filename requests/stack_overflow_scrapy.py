from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

class Pregunta(Item):
  id = Field()
  pregunta = Field()
  descripcion = Field()


class StackOverflowSpider(Spider):
  name = "MiPrimerSpider"
  custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
      (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 \
      Safari/537.36'
  }

  start_urls = ['https://stackoverflow.com/questions']

  def parse(self, response):
    sel = Selector(response)
    preguntas = sel.xpath('//div[@id="questions"]//div[contains(@class, "s-post-summary")]')
    id = 0
    for pregunta in preguntas:
      item = ItemLoader(Pregunta(), pregunta)
      item.add_xpath('pregunta', './/h3/a/text()')
      item.add_xpath('descripcion', './/div[@class="s-post-summary--content-excerpt"]/text()')
      item.add_value('id', id)
      id += 1

      yield item.load_item()