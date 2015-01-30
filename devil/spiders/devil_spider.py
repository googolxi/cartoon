# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from devil.items import ComicItem, EpItem
import re


class DevilSpider(scrapy.Spider):
    name = "devil"
    allowed_domains = ['kankan.com']

    def start_requests(self):
        start_urls = [
            "http://data.movie.kankan.com/movie/60088",
        ]
        for url in start_urls:
            yield Request(url, callback=self.parse_comic)
    def parse_comic(self,response):
        item = ComicItem()
        #item['title']  = response.css("ul.base li.base_name h1::text").extract()[0]
        item['title']  = response.css("div.main div.section h1::text").extract()[0]
        #item['year'] = response.css("ul.base li.base_pub::text").extract()[0]
        year = response.css("div.main div.section h1 em::text").extract()[0]
        patt = re.compile(r'\((\d+)\)')
        item['year'] = patt.findall(year)
        #item['area'] = response.css("ul.params li.short span::text").extract()[0]
        item['area'] = response.css("div#movie_basic_info ul.more li a::text").extract()[0] 
        #item['type'] = response.css("ul.params li.short span::text").extract()[1]
        type = response.css("div#movie_basic_info ul li a::text").extract()[11:18]
        item['type'] = ', '.join(type)
        #item['pic'] = "http://v.youku.com/v_show/id_XNTE2NTg5ODU2.html"
        item['pic'] = response.css("div.section a img::attr(src)").extract()[0]
        item['desc'] = response.css("div#intro_cont_first p::text").extract()[0]
        #item['desc'] = response.css("div.detail div.intro::text").extract()[1]
        #item['hits'] = response.css("ul.stats li span::text").extract()[0]
        item['hits'] = response.css("div#movie_basic_info ul li span::text").extract()[0]
        item['ep_list'] = []
        ep_item = EpItem()
        item['ep_list'].append(ep_item)
        #ep_item['src_type'] = 2
        #ep_item['org_url'] = response.url
        #ep_item['key'] = '/'.join(response.url.split('/')[-3:-1])
        #ep_item['ep_title'] = item['title'] 
        #ep_item['ep'] = 0
        ep_one  = response.css("div.cont ul#fenji_0_asc  li")
        ep_two  = response.css("div.cont ul#fenji_1_asc  li")
        ep_three = response.css("div.cont ul#fenji_2_asc  li")
        ep_list = ep_one + ep_two + ep_three 
        print ep_list
        ep_id  = 1
        print "jiong"
        for ep in ep_one:
            ep_item = EpItem()
            ep_item['src_type'] = 1
            ep_item['org_url'] = ep.css("a::attr(href)").extract()[0]
            ep_item['ep_title'] = ep.css("a::attr(title)").extract()[0]
            ep_item['key'] = '/'.join(response.url.split('/')[-3:-2])
            ep_item['ep'] = ep_id
            ep_id +=1
            
            item['ep_list'].append(ep_item)
            item['eps'] = len(item['ep_list'])
             
            return item
