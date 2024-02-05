from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader

class Hotel(Item):
  nombre = Field()
  precio = Field()
  descripcion = Field()
  amenities = Field()

class TripAdvisor(CrawlSpider):
  name = 'Hoteles'
  custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3'
  }
  start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

  download_delay = 2# 2 segundos de espera entre cada petición

  rules = (
    Rule(
      LinkExtractor(
        allow=r'/Hotel_Review-'
      ), follow=True, callback='parse_hotel'
    ),
  )

  def quitarSimboloDolar(self, texto):
    return texto.replace('$','').strip()

  def parse_hotel(self, response):
    sel = Selector(response)
    item = ItemLoader(Hotel(), sel)

    item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
    item.add_xpath('precio', '//div[@class="aLfMd"]/text()', MapCompose(self.quitarSimboloDolar))
    item.add_xpath('descripcion', '//div[@class="_T FKffI TPznB Ci ajMTa Ps Z BB"]/div/text()')
    item.add_xpath('amenities', '//div[@data-test-target="amenity_text"]/text()')

    yield item.load_item()