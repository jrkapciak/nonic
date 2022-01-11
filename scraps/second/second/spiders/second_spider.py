import scrapy
import os
import sys
import django
import re

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../.."))
os.environ['DJANGO_SETTINGS_MODULE'] = 'nonic.settings'

django.setup()

from nonic.models import Beer, Manufacturer, Style
from scraps.settings import start_urls_second, second_base_url


class SecondSpider(scrapy.Spider):
    name = "second"

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        self.start_urls = start_urls_second

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for nav_item in response.css('.button.navItem'):
            url = f"{second_base_url}{nav_item.css('a:nth-child(1)::attr(href)').extract()[0]}"
            yield scrapy.Request(url=url, callback=self.parse_attr)

    def parse_attr(self, response):
        name = response.css("legend .navItem::text").extract()[0]
        style = response.css(".Tips1::text").extract()[0]
        alk = response.css(".tag::text")[0].extract().replace(u'\xa0', '')
        extract = response.css(".tag::text")[1].extract().replace(u'\xa0', '')
        code = response.css(".tag::text")[2].extract().replace(u'\xa0', '')
        country = response.css(".tag a::text")[1].extract()
        description = " ".join(
            response.xpath('//*[@id="intertext1"]/div[4]')[0].css("::text").extract()
        )
        print({
            "name": name,
            "style": style,
            "alk": alk,
            "extract": extract,
            "code": code,
            "country": country,
            "description": description,
        })


