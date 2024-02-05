from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader

class Articulo(Item):
  titulo = Field()
  citaciones = Field()
  autores = Field()
  url = Field()


class GoogleSchoolar(CrawlSpider):
  name = 'googleScholar'

  custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3',
    'DEPTH_LIMIT': 3,
    'FEED_EXPORT_ENCODING': 'utf-8'
  }

  allowed_domains = ['scholar.google.com']

  download_delay = 1

  start_urls = ['https://scholar.google.com/scholar?as_ylo=2023&q=AI&hl=en&as_sdt=0,5']

  rules = (
    # citado por
    Rule(
      LinkExtractor(
        allow=r'\?cites=\d+',
        restrict_xpaths='//div[@class="gs_ri"]'
      ), follow=True, callback='parse_start_url'
    ),
  )

  def cites(self, text):
    return ''.join((text.strip())[-2:])

  def parse_start_url(self, response):
    sel = Selector(response)
    articulos = sel.xpath('//div[@class="gs_ri"]')

    for articulo in articulos:
      item = ItemLoader(Articulo(), articulo)
      item.add_xpath('titulo', './/h3[@class="gs_rt"]/a/text()')
      item.add_xpath('url','.//h3/a/@href')

      autores = articulo.xpath('.//div[@class="gs_a"]//text()').getall()
      autores = (''.join(autores)).split('-')[0].strip()
      item.add_value('autores', autores)
      try:
        item.add_xpath('citaciones', './/a[contains(@href,"cites")]/text()', MapCompose(self.cites))
      except:
        item.add_value('citaciones', '0')

      yield item.load_item()