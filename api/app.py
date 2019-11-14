'''
api definition
'''

import falcon

from api import budget_ep

# create API
api = app = falcon.API(middleware=[budget_ep.CORSMiddleware()])

# create endpoints for API.
api.add_route('/api/detail_exp', budget_ep.DetailExpenditure())
api.add_route('/api/exp_summary', budget_ep.ExpenditureSummary())
api.add_route('/api/detail_exp_test', budget_ep.DetailExpenditure01())
api.add_route('/api/detail_exp_week', budget_ep.DetailExpenditureWeek())
api.add_route('/api/acc_heads', budget_ep.AccountHeads())