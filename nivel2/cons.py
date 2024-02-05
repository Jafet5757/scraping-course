from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader

class Departamento(Item):
  nombre = Field()
  direccion = Field()

class Urbaniape(CrawlSpider):
  name = 'Urbaniape'

  custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3',
    'FEED_EXPORT_ENCODING': 'utf-8',
    'CLOSESPIDER_ITEMCOUNT':24
  }

  download_delay = 1

  start_urls = [
    'https://urbania.pe/buscar/proyectos-propiedades?page=1',
    'https://urbania.pe/buscar/proyectos-propiedades?page=2',
    'https://urbania.pe/buscar/proyectos-propiedades?page=3',
    'https://urbania.pe/buscar/proyectos-propiedades?page=4',
    'https://urbania.pe/buscar/proyectos-propiedades?page=5'
  ]

  allowed_domains = ['urbania.pe']

  rules = (
    Rule(
      LinkExtractor(
        allow=r'/proyecto-'
      ), follow=True, callback='parse_depa'
    ),
  )

  def parse_depa(self, response):
    sel = Selector(response)
    item = ItemLoader(Departamento(), sel)

    item.add_xpath('nombre', '//h1[@class="title-h1-development"]/text()')
    item.add_xpath('direccion', '//h4[@id="ref-map"]/text()')

    yield item.load_item()