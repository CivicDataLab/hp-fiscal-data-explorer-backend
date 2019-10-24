'''
budget data endpoints
'''
import json
from datetime import datetime

import falcon
from api.db import connection

def validate_date(req, resp, resource, params):


def validate_date(req, resp, resource, params):
    '''
    check for required parameters in query string and validate date format.
    '''
    params = req.params
    if 'start' not in params or 'end' not in params:
        resp.status = falcon.HTTP_400  #pylint: disable=no-member
        raise falcon.HTTPBadRequest('Incomplete Request', 'start and end date is required')  #pylint: disable=no-member
    try:
        datetime.strptime(params['start'], '%Y-%m-%d')
        datetime.strptime(params['end'], '%Y-%m-%d')
    except ValueError as err:
        resp.status = falcon.HTTP_400  #pylint: disable=no-member
        raise falcon.HTTPBadRequest('Invalid Params', str(err))  #pylint: disable=no-member

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

        query_string = "select * from himachal_budget_allocation_expenditure WHERE date BETWEEN '{}' and '{}'"  # pylint: disable=line-too-long
        query = CONNECTION.execute(query_string.format(start, end))
        data_rows = query.fetchall()

        response_data = {'records': []}
        for row in data_rows:
            record = {}
            date = datetime.strftime(row[11], '%Y%m%d')
            record['demand'] = row[1]
            record['major'] = row[2]
            record['sub_major'] = row[3]
            record['minor'] = row[4]
            record['sub_minor'] = row[5]
            record['budget'] = row[6]
            record['voted_charged'] = row[7]
            record['plan_nonplan'] = row[8]
            record['soe'] = row[9]
            record['soe_desc'] = row[10]
            record['date'] = date
            record['sanction'] = row[12]
            record['addition'] = row[13]
            record['savings'] = row[14]
            record['revised'] = row[15]

            response_data['records'].append(record)


        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = json.dumps(response_data)
