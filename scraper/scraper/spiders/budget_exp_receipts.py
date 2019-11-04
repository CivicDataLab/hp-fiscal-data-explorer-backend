'''
Budget expenditure and receitps spiders
'''
# -*- coding: utf-8 -*-
from scraper.spiders import budget_base


class BudgetExpendituresSpider(budget_base.ExpenditureBaseSpider):
    '''
    BudgetReceiptsSpider
    '''
    name = 'budget_expenditures'

    start_urls = ['http://himkosh.hp.nic.in/treasuryportal/eKosh/ekoshhodAllocationquery.asp']

    # dataset is collected from here.
    query_url = 'http://himkosh.hp.nic.in/treasuryportal/eKosh/eKoshHODAllocationPopUp.asp?{}'

    query_index = 9

    unit = '.00001'

class BudgetReceiptsSpider(budget_base.ReceiptBaseSpider):
    '''
    BudgetReceiptsSpider
    '''
    name = 'budget_receipts'

    # dataset is collected from here.
    query_url = 'https://himkosh.nic.in/eHPOLTIS/PublicReports/Receipt.asmx/GetReceiptMajorDetail'

    unit = '1'
