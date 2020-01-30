'''
api definition
'''

import falcon

from api import budget_ep, receipts, schemes

# create API
api = app = falcon.API(middleware=[budget_ep.CORSMiddleware(), receipts.CORSMiddleware()])

# create endpoints for API.
api.add_route('/api/exp_summary', budget_ep.ExpenditureSummary())
api.add_route('/api/detail_exp_week', budget_ep.DetailExpenditureWeek())
api.add_route('/api/detail_exp_month', budget_ep.DetailExpenditureMonth())
api.add_route('/api/acc_heads', budget_ep.DetailAccountHeads())
api.add_route('/api/acc_heads_test', budget_ep.DetailAccountHeadsTest())
api.add_route('/api/acc_heads_desc', budget_ep.DetailAccountHeadsDesc())
api.add_route('/api/unique_acc_heads', budget_ep.UniqueAccountHeads())
api.add_route('/api/unique_acc_heads_treasury', budget_ep.UniqueAccountHeadsTreasury())
api.add_route('/api/unique_acc_heads_schemes', schemes.UniqueAccountHeadsSchemes())
api.add_route('/api/detail_receipts_week', receipts.DetailReceiptsWeek())
api.add_route('/api/detail_receipts_month', receipts.DetailReceiptsMonth())
api.add_route('/api/treasury_exp', budget_ep.TreasuryExpenditureVisType())
api.add_route('/api/treasury_exp_week', budget_ep.TreasuryExpenditureWeek())
api.add_route('/api/acc_heads_treasury', budget_ep.TreasuryAccountHeads())
api.add_route('/api/acc_heads_receipts', receipts.ReceiptsAccountHeads())
api.add_route('/api/acc_heads_schemes',schemes.SchemesAccountHeads())
api.add_route('/api/schemes', schemes.SchemesVisType())
