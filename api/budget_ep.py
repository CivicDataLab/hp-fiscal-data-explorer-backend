'''
budget data endpoints
'''
import json
from datetime import datetime
import falcon
from api.db import connection

def validate_date(req, resp, resource, params):

    params = req.params
    if 'start' not in params or 'end' not in params:
        resp.status = falcon.HTTP_400
        raise falcon.HTTPBadRequest('Incomplete Request', 'start and end date is required')
    try:
        start = datetime.strptime(params['start'], '%Y-%m-%d')
        end = datetime.strptime(params['end'], '%Y-%m-%d')
    except ValueError as err:
        resp.status = falcon.HTTP_400
        raise falcon.HTTPBadRequest('Invalid Params', str(err))

@falcon.before(validate_date)
class DetailExpenditure():
    '''
    detail exp
    '''
    def on_get(self, req, resp):
        '''
        method for getting detail expenditure
        '''
        params = req.params
        start = datetime.strptime(params['start'], '%Y-%m-%d')
        end = datetime.strptime(params['end'], '%Y-%m-%d')

        query_string = "select * from himachal_budget_allocation WHERE date BETWEEN '{}' and '{}'"
        query = connection.execute(query_string.format(start, end))
        data_rows = query.fetchall()

        response_data = {'records': []}
        for row in data_rows:
            record = {}
            date = datetime.strftime(row[10], '%Y%m%d')
            record['demand'] = row[0]
            record['major'] = row[1]
            record['sub_major'] = row[2]
            record['minor'] = row[3]
            record['sub_minor'] = row[4]
            record['budget'] = row[5]
            record['voted_charged'] = row[6]
            record['plan_nonplan'] = row[7]
            record['soe'] = row[8]
            record['soe_desc'] = row[9]
            record['date'] = date
            record['sanction'] = row[11]
            record['addition'] = row[12]
            record['savings'] = row[13]
            record['revised'] = row[14]

            response_data['records'].append(record)


        resp.status = falcon.HTTP_200
        resp.body = json.dumps(response_data)