# -*- coding: utf-8 -*-
from scraper.spiders import treasury_base


class TreasuryExpendituresSpider(treasury_base.TreasuryBaseSpider):
    name = 'treasury_expenditures'

    start_urls = ['https://himkosh.hp.nic.in/treasuryportal/eKosh/ekoshddoquery.asp']

    # dataset is collected from here.
    query_url = 'https://himkosh.hp.nic.in/treasuryportal/eKosh/eKoshDDOPopUp.asp?{}'

    query_index = 10


class TreasuryReceiptsSpider(treasury_base.TreasuryBaseSpider):
    name = 'treasury_receipts'

    start_urls = ['https://himkosh.hp.nic.in/treasuryportal/eKosh/eKoshDDOReceiptQuery.asp']

    # dataset is collected from here.
    query_url = 'https://himkosh.hp.nic.in/treasuryportal/eKosh/eKoshDDOReceiptPopUp.asp?{}'

    query_index = 1
