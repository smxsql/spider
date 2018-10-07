# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
from ArticleSpider.items import JoBoleArticleItem,ArticleItemLoader
from ArticleSpider.utils.common import get_md5
class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    # 允許的域名
    allowed_domains = ['blog.jobbole.com']
    # 起始的url
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        獲取列表頁的所有url然後把url交給scrapy進行下載
        獲取列表頁的下一頁
        :param response:
        :return:
        """
        # 獲取列表頁的url,下面使用的url的嵌套
        nodes = response.css("#archive .floated-thumb .post-thumb a")
        for node in nodes:
            url = node.css("::attr(href)").extract_first("")
            image_url = node.css("img::attr(src)").extract_first("")
            # 用urllib中的parse進行url拼接 yield會自動把這個拼接好的url交給我們的url進行下載
            yield Request(url=parse.urljoin(response.url,url),meta={"front_image_url":image_url},callback=self.parse_detail)

        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)

    def parse_detail(self,response):
        article_item = JoBoleArticleItem()
        # 提取文章的具體字段,這個就是回調函數
        # 這個是載瀏覽器上復制的
        # //*[ @ id = "post-114430"]/div[1]/h1
        # 這個是自己分析的
        # /html/body/div[3]/div[3]/div[1]/div[1]/h1
        # re_selector = response.xpath("/html/body/div[1]/div[3]/div[1]/div[1]/h1")
        # re_selector =  response.xpath("//*[ @ id = \"post-114430\"]/div[1]/h1/text()")
        # 當數組中出現空的時候extract_first()不會報異常
        # title = response.xpath("//div[@class='entry-header']/h1/text()").extract_first()
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace(" ·", "")
        # praise_nums = int(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0])
        # fav_nums = int(response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0].replace(" 收藏","").strip())
        # comment_num = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # match_re = ('.*(\d+).*',comment_num)
        # if match_re:
        #     comment_num = match_re.group(1)
        # content = response.xpath("//div[@class='entry']").extract()[0]


        #通過css選擇器提取字段
        # 文章封面圖
        front_image_url = response.meta.get("front_image_url","")
        # title = response.css(".entry-header h1::text").extract()[0]
        # create_date =  response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip().replace(" ·","")
        # praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        # fav_nums = response.css(".bookmark-btn::text").extract()[0].strip()
        # match_re = re.match(".*?(\d+).*",fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        # comment_num = response.css("a[href='#article-comment'] span::text").extract()[0]
        # match_re = re.match('.*?(\d+).*',comment_num)
        # if match_re:
        #     comment_num = int(match_re.group(1))
        # else:
        #     comment_num = 0
        # content = response.css("div.entry").extract()[0]
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["title"] = title
        # article_item["url"] = response.url
        # try:
        #     create_date = datetime.datetime.strptime(create_date,"%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item["create_date"] = create_date
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_nums"] = praise_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["comment_num"] = comment_num
        # article_item["content"] = content


        # 通過item Loader加載item
        item_loader = ArticleItemLoader(item=JoBoleArticleItem(),response=response)
        # 這樣就是把值選擇之後再加載進來
        item_loader.add_css('title',".entry-header h1::text")
        # item_loader.add_xpath()
        item_loader.add_value("url",response.url)
        item_loader.add_value("url_object_id",get_md5(response.url))
        item_loader.add_css("create_date",".entry-meta-hide-on-mobile::text")
        item_loader.add_css("praise_nums",".vote-post-up h10::text")
        item_loader.add_css("fav_nums",".bookmark-btn::text")
        item_loader.add_css("comment_num","a[href='#article-comment'] span::text")
        item_loader.add_css("content","div.entry")
        item_loader.add_value("front_image_url",[front_image_url])

        # 獲取解析後的item對象
        article_item = item_loader.load_item()

        yield article_item
        # 此時就會傳到我們的pipelines中





