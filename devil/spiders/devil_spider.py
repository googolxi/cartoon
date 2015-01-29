# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from devil.items import ComicItem, EpItem
import re


class DevilSpider(scrapy.Spider):
    name = "devil"
    #allowed_domains = ['soku.com']

    def start_requests(self):
        start_urls = [
            "http://www.soku.com/detail/show/XNDQ0NDEy",
        ]
        for url in start_urls:
            yield Request(url, callback=self.parse_comic)
    def parse_comic(self,response):
        item = ComicItem()
        item['title']  = response.css("ul.base li.base_name h1::text").extract()[0]
        item['year'] = response.css("ul.base li.base_pub::text").extract()[0]
        item['area'] = response.css("ul.params li.short span::text").extract()[0]
        item['type'] = response.css("ul.params li.short span::text").extract()[1]
        item['pic'] = "http://v.youku.com/v_show/id_XNTE2NTg5ODU2.html"
        item['desc'] = response.css("div.detail div.intro::text").extract()[1]
        item['hits'] = response.css("ul.stats li span::text").extract()[0]
        item['ep_list'] = []
        ep_item = EpItem()
        #ep_item['src_type'] = 2
        #ep_item['org_url'] = response.url
        #ep_item['key'] = '/'.join(response.url.split('/')[-3:-1])
        #ep_item['ep_title'] = item['title'] 
        #ep_item['ep'] = 0
        item['ep_list'].append(ep_item)
        eplist_url_patt = 'http://v.youku.com/v_show/id_XNTE2NTg5ODU2.html'
        yield Request(eplist_url_patt,meta={'item':item},callback=self.parse_ep_list)
    def parse_ep_list(self,response):
        item = response.meta['item']
        ep_list = response.css("div.textlists div.lists ul.items li")[:52]
        #print ep_list
        print "world"
        ep_id = 1 
        print ep_id
        for ep in ep_list:
            ep_item = EpItem()
            ep_item['src_type'] = 1
            ep_item['org_url'] = ep.css("a::attr(href)").extract()[0]
            print "hello"
            ep_item['key'] =  '/'.join(response.url.split('/')[-3:-2])
            ep_item['ep_title'] = ep.css("a span.l_title::text").extract()[0]
            ep_item['ep'] = ep_id
            
            ep_id +=1
        
            item['ep_list'].append(ep_item)
            item['eps'] = len(item['ep_list'])
        return item
