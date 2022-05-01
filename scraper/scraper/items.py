import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def clean_spaces(string):
    return " ".join(string.split())

def clean_price(string):
    string = string.replace("$", "")
    string = string.replace(".", "")
    return string

class ScraperItem(scrapy.Item):
    """
    Item Loader class.
    """
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags, clean_spaces),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, clean_spaces, clean_price),
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags, clean_spaces),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
