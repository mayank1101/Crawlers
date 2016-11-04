import scrapy
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from astro.items import AstroItem
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
import re


class AstronomySpider(scrapy.Spider):
    name = 'astro'

    start_urls = ['http://astronomy.stackexchange.com/',]

    def parse(self, response):
        href = response.xpath('//a[@id="home-browse"]/@href').extract_first()
        yield scrapy.Request(response.urljoin(href), callback = self.get_all_data)


    def get_all_data(self,response):
        bsObj = BeautifulSoup(response.body,"lxml")
        id_list = []

        # extracting each div id and storing in a list
        for tags in bsObj.findAll("div", {"id":re.compile("^question(|-|)summary(|-|)[0-9]{2,4}")}):
            id_list.append(tags["id"])
        for ids in id_list:
            load = ItemLoader(AstroItem(),response=response)
            load.add_xpath('links', '//div[@id="questions"]/div[@id="{0}"]/div[@class="summary"]/h3/a[contains(@href, "/questions")]/@href'.format(ids))
            load.add_xpath('questions', '//div[@id="questions"]/div[@id="{0}"]/div[@class="summary"]/h3/a/text()'.format(ids))
            load.add_xpath('votes', '//div[@id="questions"]/div[@id="{0}"]/div[@class="statscontainer"]/div[@class="stats"]/div[@class="vote"]/div[@class="votes"]/span[@class="vote-count-post "]/strong/text()'.format(ids))
            load.add_xpath('no_answers', '//div[@id="questions"]/div[@id="{0}"]/div[@class="statscontainer"]/div[@class="stats"]/div[@class="status answered"]/strong/text()'.format(ids))
            load.add_xpath('tags','//div[@id="questions"]/div[@id="{0}"]/div[@class="summary"]/div[contains(@class, "tags t-")]/a[contains(@class,"post-tag")]/text()'.format(ids))
            yield load.load_item()
            """yield{
                response.xpath('//div[@id="questions"]/div[@id="{0}"]/div[@class="summary"]/h3/a[contains(@href, "/questions")]/@href'.format(ids)).extract_first()
                response.xpath('//div[@id="questions"]/div[@id="{0}"]/div[@class="summary"]/h3/a/text()'.format(ids)).extract_first()
                response.xpath('//div[@id="questions"]/div[@id="{0}"]/div[@class="statscontainer"]/div[@class="stats"]/div[@class="vote"]/div[@class="votes"]/span[@class="vote-count-post "]/strong/text()'.format(ids)).extract_first()
                response.xpath('//div[@id="questions"]/div[@id="{0}"]/div[@class="statscontainer"]/div[@class="stats"]/div[@class="status answered"]/strong/text()'.format(ids)).extract_first()
                response.xpath('//div[@id="questions"]/div[@id="{0}"]/div[@class="summary"]/div[contains(@class, "tags t-")]/a[contains(@class,"post-tag")]/text()'.format(ids)).extract_first()
            }"""

        # retrieving next page
        next_page = response.xpath('//div[@id="mainbar"]/div[@class="pager fl"]/a[contains(@rel,"next")]/@href').extract_first()
        if next_page is not None:
            url = response.url
            new_url = url[:35] + next_page[1:]
            yield scrapy.Request(new_url, callback = self.get_all_data)
