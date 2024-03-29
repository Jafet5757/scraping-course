from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader

class Articulo(Item):
  titulo = Field()
  contenido = Field()

class Review(Item):
  titulo = Field()
  calificacion = Field()

class Video(Item):
  titulo = Field()
  fecha_publicacion = Field()

class IGNCrawler(CrawlSpider):
  name = 'ign'

  custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3',
    'CLOSESPIDER_PAGECOUNT':60
  }

  allowed_domains = ['latam.ign.com']

  download_delay = 1

  start_urls = ['https://latam.ign.com/se/?type=news&q=ps5&order_by=']

  rules = (
    # horizontalidad por tipo de informacion
    Rule(
      LinkExtractor(
        allow=r'type='
      ), follow=True
    ),
    # horizontal por paginacion
    Rule(
      LinkExtractor(
        allow=r'&page=\d+'
      ), follow=True
    ),
    # reviews
    Rule(
      LinkExtractor(
        allow=r'/review/'
      ), follow=True, callback='parse_review'
    ),
    # videos
    Rule(
      LinkExtractor(
        allow=r'/video/'
      ), follow=True, callback='parse_video'
    ),
    # news
    Rule(
      LinkExtractor(
        allow=r'/news/'
      ), follow=True, callback='parse_news'
    ),
  )

  def parse_news(self, response):
    item = ItemLoader(Articulo(), response)
    item.add_xpath('titulo', '//h1[@id="id_title"]/text()')
    item.add_xpath('contenido', '//div[@id="id_text"]//*/text()')

    yield item.load_item()

  def parse_review(seld, response):
    item = ItemLoader(Review(), response)
    item.add_xpath('titulo', '//div[@class="article-headline"]//h1/text()')
    item.add_xpath('calificacion', '//div[@class="review"]//span//span/div/text()')

    yield item.load_item()

  def parse_video(self, response):
    item = ItemLoader(Video(), response)
    item.add_xpath('titulo','//h1[@class="title"]/text()')
    item.add_xpath('fecha_publicacion', '//span[@class="publish-date"]/text()')

    yield item.load_item()