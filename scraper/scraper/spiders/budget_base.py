# -*- coding: utf-8 -*-
import scrapy
import re
import pdb

class BudgetbasespiderSpider(scrapy.Spider):
    name = 'budget_crawler'
    allowed_domains = ['ebudget.hp.nic.in']
    start_urls = ['https://ebudget.hp.nic.in/BudHome.aspx/']
    
    def parse(self, response):
        result = response.css('#tab-content1 ul li:nth-of-type(2) p.pa a::attr(onclick)').extract()
        filename = response.css('#tab-content1 ul li:nth-of-type(2) p.pa a::text').extract()
        result_receipts = response.css('#tab-content ul li:nth-of-type(8) p.pa a::attr(onclick)').extract()
        filename_receipts = response.css('#tab-content ul li:nth-of-type(8) p.pa a::text').extract()


        for i in range(len(result)):
            
            pdf_url = re.findall(".*\('(.*)'\)", result[i])
            pdf_name = filename[i]  
            yield response.follow(pdf_url[0], self.save_pdf, meta={'pdf_name': pdf_name})
        
        for i in range(len(result_receipts)):

            pdf_url_receipts = re.findall(".*\('(.*)'\)", result_receipts[i])
            pdf_name_receipts  = filename_receipts[i]  
            yield response.follow(pdf_url_receipts[0], self.save_pdf_receipts, meta={'pdf_name_receipts': pdf_name_receipts})
               
    	    
    def save_pdf(self, response):
        pdf_names = '../../datasets/budget/' + response.meta['pdf_name'] + '.pdf'
        file = open(pdf_names, 'wb')
        file.write(response.body)
        file.close()


    def save_pdf_receipts(self, response):
        pdf_names = '../../datasets/receipts/' + response.meta['pdf_name_receipts'] + '.pdf'
        file = open(pdf_names, 'wb')
        file.write(response.body)
        file.close()
    
    
 

       
       
       