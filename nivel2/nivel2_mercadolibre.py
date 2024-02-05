from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader

class Articulo(Item):
  titulo = Field()
  precio = Field()
  descripcion = Field()


class MercadoLibreCrawler(CrawlSpider):
  name = 'mercadolibre'

  custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3',
    'CLOSESPIDER_PAGECOUNT': 20
  }

  download_delay = 1

  # Restringimos la busqueda con los dominios permitidos
  allowed_domains = ['listado.mercadolibre.com.mx', 'www.mercadolibre.com.mx']

  start_urls = ['https://listado.mercadolibre.com.mx/celulares-telefonia/celulares-smartphones/iphone-14_NoIndex_True']

  rules = (
    # paginacion
    Rule(
      LinkExtractor(
        allow = r'/iphone-14_Desde_'
      ), follow=True
    ),
    # Detalles de preguntas
    Rule(
      LinkExtractor(
        allow = r'/MLM'
      ), follow=True, callback='parse_items'
    ), 
  )

  def parse_items(self, response):
    item = ItemLoader(Articulo(), response)
    item.add_xpath('titulo', '//h1[@class="ui-pdp-title"]/text()')
    item.add_xpath('descripcion', '//p[@class="ui-pdp-description__content"]/text()')
    item.add_xpath('precio', '//div[@class="ui-pdp-price__second-line"]//span[@class="andes-money-amount__fraction"]/text()')

    yield item.load_item()