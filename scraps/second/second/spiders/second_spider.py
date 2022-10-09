import os
import re
import sys

import django
import scrapy

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../.."))
os.environ["DJANGO_SETTINGS_MODULE"] = "nonic.settings"

django.setup()

from nonic.models import Beer, BeerSource, Manufacturer, Style

from ..settings import manufacture_url, s1_phrase, second_base_url, start_urls_second


class SecondSpider(scrapy.Spider):
    name = "second"

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        self.start_urls = start_urls_second
        self.manufacturers_map = {}

    def start_requests(self):
        yield scrapy.Request(url=manufacture_url, callback=self.parse_manufacturers)

    def parse(self, response):
        for nav_item in response.css(".button.navItem"):
            if s1_phrase in nav_item.extract():
                if resource_url_list := nav_item.css("a:nth-child(1)"):
                    resource_url = resource_url_list.css("::attr(href)").extract()[0]
                else:
                    resource_url = nav_item.css("a::attr(href)").extract()[0]

                url = f"{second_base_url}{resource_url}"
                if BeerSource.objects.filter(url=url).exists():
                    continue
                else:
                    yield scrapy.Request(url=url, callback=self.parse_attr)

    def parse_manufacturers(self, response):
        for manufacturer in reversed(response.css("#main div")):
            if resource_url := manufacturer.css("a:contains('zobacz wszystkie »')::attr(href)"):
                manufacturer_url = f"{second_base_url}{resource_url[0].extract()}"
                manufacturer_name = manufacturer.css("h3::text").extract()[0]
                manufacturer_name = manufacturer_name.replace("Sp. z o.o.", "")
                manufacturer_name = manufacturer_name.replace("Sp z o.o.", "")
                manufacturer_name = manufacturer_name.replace("S.A", "")
                manufacturer_name = manufacturer_name.replace("s.c.", "")
                manufacturer_name = manufacturer_name.replace("Spółka Jawna", "")
                manufacturer_name = manufacturer_name.strip()
                manufacturer = Manufacturer.objects.filter(name__icontains=manufacturer_name).first()
                if not manufacturer:
                    manufacturer = Manufacturer.objects.create(name=manufacturer_name)
                yield scrapy.Request(
                    url=manufacturer_url,
                    callback=self.parse_manufacturer_products_list,
                    meta={"manufacturer": manufacturer},
                )

    def parse_manufacturer_products_list(self, response):
        for nav_item in response.css(".button.navItem"):
            if s1_phrase in nav_item.extract():
                if resource_url_list := nav_item.css("a:nth-child(1)"):
                    resource_url = resource_url_list.css("::attr(href)").extract()[0]
                else:
                    resource_url = nav_item.css("a::attr(href)").extract()[0]

                url = f"{second_base_url}{resource_url}"

                if BeerSource.objects.filter(url=url).exists():
                    continue
                else:
                    yield scrapy.Request(
                        url=url, callback=self.parse_attr, meta={"manufacturer": response.meta.get("manufacturer")}
                    )

    def parse_attr(self, response):
        result = {}
        result["code"] = response.css(".tag::text")[2].extract().replace("\xa0", "")

        if not result["code"]:
            return

        if Beer.objects.filter(code=result["code"]).first():
            return

        result["manufactured_by"] = response.meta.get("manufacturer")
        result["name"] = response.css("legend .navItem::text").extract()[0]
        style = response.css(".Tips1::text").extract()
        try:
            styles = []
            for style_name in style:
                style, _ = Style.objects.get_or_create(name__iexact=style_name, defaults={"name": style_name})
                styles.append(style.id)
        except:
            styles = None
        if raw_alcohol := response.css(".tag::text")[0].extract():
            if not raw_alcohol.replace(" ", ""):
                pass
            try:
                result["alcohol"] = re.findall(r"[-+]?\d*\.?\d+|\d+", raw_alcohol)[0]
            except IndexError:
                pass

        if extract_raw := response.css(".tag::text")[1].extract():
            if not extract_raw.replace(" ", ""):
                pass
            else:
                try:
                    result["extract"] = re.findall(r"[-+]?\d*\.?\d+|\d+", raw_alcohol)[0]
                except IndexError:
                    pass

        result["country"] = response.css(".tag a::text")[1].extract()
        result["description"] = " ".join(response.xpath('//*[@id="intertext1"]/div[4]')[0].css("::text").extract())
        beer, _ = Beer.objects.get_or_create(code=result["code"], defaults=result)

        if styles:
            beer.style.add(*styles)
        BeerSource.objects.update_or_create(beer=beer, defaults={"url": response.url})
        return
