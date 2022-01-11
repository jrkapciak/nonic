import scrapy
import os
import sys
import django
import re

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../.."))
os.environ['DJANGO_SETTINGS_MODULE'] = 'nonic.settings'

django.setup()

from nonic.models import Beer, Manufacturer, Style
from scraps.settings import start_urls_first


class FirstSpider(scrapy.Spider):
    name = "first"

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        self.start_urls = start_urls_first

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for nav_item in response.css('.image-fade_in_back'):
            url = nav_item.css('a:nth-child(1)::attr(href)').extract()[0]
            yield scrapy.Request(url=url, callback=self.parse_attr)

    def parse_attr(self, response):
        manufacturer_name = response.css('.posted_in a::text').extract()[0].replace(u'\xa0', ' ')
        manufacture, _ = Manufacturer.objects.get_or_create(
            name=manufacturer_name
        )
        name = response.css('.product-title.entry-title::text').extract()[0].replace(u'\xa0', ' ').strip()

        if Beer.objects.filter(name=name).exists():
            return

        description = response.css('.product-short-description p::text').extract()
        if description:
            description = description[0].replace(u'\xa0', ' ')

        code = response.css('.sku::text').extract()
        if code:
            code = code[0].replace(u'\xa0', ' ')

        if not code:
            return

        result = {
            'name': name,
            'code': response.css('.sku::text').extract()[0].replace(u'\xa0', ' '),
            'description': description,
            'manufactured_by': manufacture
        }
        labels = response.css('.woocommerce-product-attributes-item__label')
        values = response.css('.woocommerce-product-attributes-item__value')
        attrs = {}
        styles = []
        for num, label in enumerate(labels, start=0):
            try:
                attrs[label.css('::text').extract()[0]] = values[num].css('p a::text').extract()[0]
            except IndexError:
                attrs[label.css('::text').extract()[0]] = values[num].css("td::text").extract_first()

            if label.css('::text').extract()[0] == "Pojemność butelki":
                try:
                    result["volume"] = int(re.findall(r'\d+', values[num].css('p a::text').extract()[0])[0])
                except:
                    pass

            if label.css('::text').extract()[0] == "Rodzaj piwa":
                try:
                    style_names = values[num].css('p a::text').extract()
                    styles = []
                    for style_name in style_names:
                        style, _ = Style.objects.get_or_create(
                            name=style_name
                        )
                        styles.append(style.id)
                except:
                    pass
            if label.css('::text').extract()[0] == "Alkohol (%)":
                result['alcohol'] = float(values[num].css('p a::text').extract()[0].replace(",", '.'))
            if label.css('::text').extract()[0] == "Ekstrakt":
                result['extract'] = float(values[num].css('p a::text').extract()[0].replace(",",'.'))

        result['tags'] = attrs
        beer, _ = Beer.objects.update_or_create(name=result["name"], defaults=result)
        if styles:
            beer.style.add(*styles)
