# -*- coding: utf-8 -*-
import scrapy


class TreasuryBaseSpider(scrapy.Spider):
    allowed_domains = ['himkosh.hp.nic.in']

    def parse(self, response):
        pass
