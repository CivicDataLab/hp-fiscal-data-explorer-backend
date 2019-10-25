'''
api definition
'''

import falcon

from api import budget_ep

# create API
api = app = falcon.API()

# create endpoints for API.
api.add_route('/api/detail_exp', budget_ep.DetailExpenditure())
api.add_route('/api/exp_summary', budget_ep.ExpenditureSummary())