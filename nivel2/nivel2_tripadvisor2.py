from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader

class Opinion(Item):
  titulo = Field()
  calificacion = Field()
  contenido = Field()
  contenido = Field()
  autor = Field()

class TripAdvisor(CrawlSpider):
  name = 'OpinionestripAdvisor'
  custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3',
    'CLOSESPIDER_PAGECOUNT': 100
  }

  allowed_domains = ['tripadvisor.com']
  start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

  download_delay = 1

  rules = (
    # Paginacion de hoteles (h)
    Rule(
      LinkExtractor(
        allow=r'-oa\d+-'
      ), follow=True
    ),
    # Detalle de hoteles (v)
    Rule(
      LinkExtractor(
        allow=r'/Hotel_Review-',
        restrict_xpaths=['//div[@data-automation="hotel-card-title"]']
      ), follow=True
    ),
    # Paginacion de opiniones (h)
    Rule(
      LinkExtractor(
        allow=r'-or\d+-'
      ), follow=True
    ),
    # Detalle de perfil (v)
    Rule(
      LinkExtractor(
        allow=r'/Profile/',
        restrict_xpaths=['//div[@data-test-target="HR_CC_CARD"]//a[1]']
      ), follow=True, callback='parse_opinion'
    )
  )

  def obtenercalificacion(self, texto):
    return str(texto[-2])

  def parse_opinion(self, reponse):
    sel = Selector(reponse)
    opiniones = sel.xpath('//div[@id="content"]/div/div')
    autor = sel.xpath('//h1[1]/span/text()').get()

    for opinion in opiniones:
      item = ItemLoader(Opinion(), opinion)
      item.add_xpath('titulo', './/div[@class="AzIrY b _a VrCoN"]/text()')
      item.add_xpath('calificacion', './/div[@class="wnqnF"]//span[contains(@class,"ui_bubble_rating")]/@class', MapCompose(self.obtenercalificacion))
      item.add_xpath('contenido', './/div[@class="JnUAZ"]//div[@class="muQub VrCoN"]/*/text()')
      item.add_value('autor', autor)

      yield item.load_item()