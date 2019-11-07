'''
budget data endpoints
'''
import json
from datetime import datetime
import pdb
import falcon
from io import StringIO
from api.db import CONNECTION
import pandas as pd




class CORSMiddleware:
    def process_request(self, req, resp):
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
        io = StringIO()
        data = json.dump(response_data, io)
        resp.body = io.getvalue()

        

class ExpenditureSummary():
    """Expenditure Summary"""

    def on_get(self, req, resp):

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
        io = StringIO()
        data = json.dump(list_, io)
        resp.body = io.getvalue()

@falcon.before(validate_date)
class DetailExpenditureWeek():
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
        query_string = "select * from himachal_budget_allocation_expenditure WHERE date BETWEEN '{}' and '{}'" .format(start,end) # pylint: disable=line-too-long
        budget_hoa = pd.read_sql(query_string, CONNECTION, parse_dates = ['date'])
        budget_hoa = budget_hoa.groupby(['demand','major','sub_major','minor','sub_minor','budget','voted_charged','plan_nonplan','SOE','SOE_description', pd.Grouper(key='date', freq='W-MON')])[['SANCTION','ADDITION','SAVING','REVISED']].sum().reset_index().sort_values('date')
        budget_hoa['date'] = budget_hoa['date'].dt.strftime('%Y-%m-%d')
        budget_hoa.reset_index(drop = True, inplace = True)
        
        response_data_df = budget_hoa.to_json(orient = 'values')
        data_response =  json.dumps(response_data_df)
        json_response_week_wise = data_response.replace("\\","");
       
            
        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        io = StringIO()
        resp.body = json_response_week_wise
        