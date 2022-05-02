import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import replace_tags


def clean_string(string):
    return " ".join(replace_tags(string, token=" ").split())

def clean_price(string):
    string = replace_tags(string)
    string = string.replace("$", "")
    string = string.replace(".", "")
    return " ".join(string.split())

class ScraperItem(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(clean_string),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(clean_price),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(clean_string),
        output_processor=TakeFirst()
    )
