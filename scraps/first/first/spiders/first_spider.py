import os
import re
import sys

import django
import scrapy

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../.."))
os.environ["DJANGO_SETTINGS_MODULE"] = "nonic.settings"

django.setup()

from nonic.models import Beer, BeerSource, Manufacturer, Style
from ..settings import start_url_first


class FirstSpider(scrapy.Spider):
    name = "first"

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        self.start_urls = start_url_first

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for nav_item in response.css(".image-fade_in_back"):
            url = nav_item.css("a:nth-child(1)::attr(href)").extract()[0]
            if BeerSource.objects.filter(url=url).exists():
                continue
            else:
                yield scrapy.Request(url=url, callback=self.parse_attr)

    def parse_attr(self, response):
        manufacturer_name = response.css(".posted_in a::text").extract()[0].replace("\xa0", " ")
        manufacturer, _ = Manufacturer.objects.get_or_create(name=manufacturer_name)
        name = response.css(".product-title.entry-title::text").extract()[0].replace("\xa0", " ").strip()

        if Beer.objects.filter(name=name).exists():
            return

        description = response.css(".product-short-description p::text").extract()
        if description:
            description = description[0].replace("\xa0", " ")

        code = response.css(".sku::text").extract()
        if code:
            code = code[0].replace("\xa0", " ")

        if not code:
            return

        result = {
            "name": name,
            "code": response.css(".sku::text").extract()[0].replace("\xa0", " "),
            "description": description,
            "manufactured_by": manufacturer,
        }
        labels = response.css(".woocommerce-product-attributes-item__label")
        values = response.css(".woocommerce-product-attributes-item__value")
        attrs = {}
        styles = []
        for num, label in enumerate(labels, start=0):
            try:
                attrs[label.css("::text").extract()[0]] = values[num].css("p a::text").extract()[0]
            except IndexError:
                attrs[label.css("::text").extract()[0]] = values[num].css("td::text").extract_first()

            if label.css("::text").extract()[0] == "Pojemność butelki":
                try:
                    result["volume"] = int(re.findall(r"\d+", values[num].css("p a::text").extract()[0])[0])
                except:
                    pass

            if label.css("::text").extract()[0] == "Rodzaj piwa":
                try:
                    style_names = values[num].css("p a::text").extract()
                    styles = []
                    for style_name in style_names:
                        style, _ = Style.objects.get_or_create(name__iexact=style_name, defaults={"name": style_name})
                        styles.append(style.id)
                except:
                    pass
            if label.css("::text").extract()[0] == "Alkohol (%)":
                try:
                    result["alcohol"] = float(values[num].css("p a::text").extract()[0].replace(",", "."))
                except AttributeError:
                    print(values[num].css("p a::text"))
            if label.css("::text").extract()[0] == "Ekstrakt":
                try:
                    result["extract"] = float(values[num].css("p a::text").extract()[0].replace(",", "."))
                except AttributeError:
                    print(values[num].css("p a::text"))

        result["tags"] = attrs
        beer, _ = Beer.objects.update_or_create(name=result["code"], defaults=result)
        if styles:
            beer.style.add(*styles)
        BeerSource.objects.update_or_create(beer=beer, defaults={"url": response.url})
