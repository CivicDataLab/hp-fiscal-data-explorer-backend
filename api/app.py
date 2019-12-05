'''
api definition
'''

import falcon

from api import budget_ep, receipts

# create API
api = app = falcon.API(middleware=[budget_ep.CORSMiddleware(), receipts.CORSMiddleware()])

# create endpoints for API.
api.add_route('/api/detail_exp', budget_ep.DetailExpenditure())
api.add_route('/api/exp_summary', budget_ep.ExpenditureSummary())
api.add_route('/api/detail_exp_test', budget_ep.DetailExpenditure01())
api.add_route('/api/detail_exp_week', budget_ep.DetailExpenditureWeek())
api.add_route('/api/detail_exp_month', budget_ep.DetailExpenditureMonth())
api.add_route('/api/acc_heads', budget_ep.AccountHeads())
api.add_route('/api/detail_receipts_week', receipts.DetailReceiptsWeek())
api.add_route('/api/treasury_exp_month', budget_ep.TreasuryExpenditureMonth())
api.add_route('/api/acc_heads_receipts', receipts.ReceiptsAccountHeads())