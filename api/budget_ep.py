'''
budget data endpoints
'''
import json
from datetime import datetime
import pandas as pd
import falcon
from api.db import CONNECTION


class CORSMiddleware:
    '''
    Middleware for handling CORS.
    '''
    def process_request(self, req, resp):
        '''
        process request to set headers.
        '''
        resp.set_header('Access-Control-Allow-Origin', '*')


#NOTE: purposefully ignoring no-member errors
# Ref https://github.com/falconry/falcon/issues/1553
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


class ExpenditureSummary():
    """Expenditure Summary"""

    def on_get(self, req, resp):
        '''
        handle get requests for expenditure summary.
        '''
        query_string = "select * from himachal_budget_expenditure_summary"  # pylint: disable=line-too-long
        query = CONNECTION.execute(query_string)
        data_rows = query.fetchall()

        response_data = {'records': []}
        for row in data_rows:
            record = {}
            record['demand'] = row[1]
            record['demand_description'] = row[2]
            record['sanction_previous'] = row[3]
            record['sanction_current'] = row[4]
            record['pct_change'] = row[5]
            response_data['records'].append(record)


        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = json.dumps(response_data)


@falcon.before(validate_date)
class DetailExpenditure01():
    '''
    detail exp
    '''
    def on_get(self, req, resp):
        '''
        method for getting detail expenditure.
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
            record['date'] = date
            record['sanction'] = row[12]
            record['addition'] = row[13]
            record['savings'] = row[14]
            record['revised'] = row[15]

            response_data['records'].append(record)
        list_ = []

        for i in response_data['records']:
            list_.append(list(i.values()))

        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = json.dumps(list_)

@falcon.before(validate_date)
class DetailExpenditureWeek():
    '''
    detail exp
    '''
    def on_post(self, req, resp):
        '''
        sample payload
        {"filters": {"major": "2011, 2216", "sub_major": "01, 02"}}
        '''
        params = req.params
        start = datetime.strptime(params['start'], '%Y-%m-%d')
        end = datetime.strptime(params['end'], '%Y-%m-%d')

        req_body = req.stream.read()
        if req_body:
            payload = json.loads(req_body)
        else:
            payload = {}

        if not payload:
            query_string = """
                SELECT sum(SANCTION), sum(ADDITION), sum(SAVING), sum(REVISED)
                FROM himachal_budget_allocation_expenditure
                WHERE date BETWEEN '{}' and '{}'
                GROUP BY WEEK(DATE(date))
            """
        else:
            select = "SELECT major, sum(SANCTION), sum(ADDITION), sum(SAVING), sum(REVISED)"
            from_str = "FROM himachal_budget_allocation_expenditure"
            where = "WHERE date BETWEEN '{}' and '{}'".format(start, end)
            groupby = "GROUP BY WEEK(DATE(date))"

            for key, value in payload['filters'].items():
                where += "AND {key} IN ({value})".format(key=key, value=value)
                groupby += ", {key}".format(key=key)

            query_string = select + ' ' + from_str + ' ' + where + ' ' + groupby

        query = CONNECTION.execute(query_string)
        data_rows = query.fetchall()
        records = []
        for row in data_rows:
            records.append(row.values())
        data_response = json.dumps({'records': records, 'count': len(records)})

        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = data_response


class AccountHeads():
    '''
    This API will give permutations and combinations of all account heads
    '''
    def on_get(self, req, resp):
        '''
        Method for getting Permutations Combinations of account heads
        '''
        query_string = "select demand,major,sub_major,minor,sub_minor,budget,plan_nonplan,voted_charged, SOE from himachal_budget_allocation_expenditure where date='2017-04-01'"  # pylint: disable=line-too-long
        query = CONNECTION.execute(query_string)
        data_account_heads = pd.read_sql(query_string, CONNECTION)
        response_data = {'demand': [],
                        'major': [],
                        'sub_major': [], 
                        'minor':[],
                        'sub_minor':[], 
                        'budget':[],
                        'plan_nonplan':[],
                        'voted_charged':[],
                        'SOE':[]}

        for i in data_account_heads.columns:
            response_data[i].append(data_account_heads[i].unique().tolist())
            
        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = json.dumps(response_data)