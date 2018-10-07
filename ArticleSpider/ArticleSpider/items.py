# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose,TakeFirst
import datetime
from scrapy.loader import ItemLoader
class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value+"-bobby"


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date

def get_nums(value):
    match_re = re.match(".*?(\d+).*",value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    # 自定義itemloader來進行拿到第一個值
    default_output_processor = TakeFirst()

class JoBoleArticleItem(scrapy.Item):
    #item只有一種類型filed而且這種類型可以存儲各種數據類型你的數據
    # input_processor就是當我們的值傳過來的時候我們可以對這個值進行預處理
    title = scrapy.Field(
        input_processor = MapCompose(lambda x:x+"-jobbole",add_jobbole)
    )
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert),
        # 調用這個類的話就會取這個列表的第一個
        output_processor = TakeFirst(),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor = MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
