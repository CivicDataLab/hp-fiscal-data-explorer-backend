import falcon

import budget_ep 

# create API
api = app = falcon.API()

# create endpoints for API.
api.add_route('/detail_exp', budget_ep.DetailExpenditure())