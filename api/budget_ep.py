'''
budget data endpoints
'''
import json
from datetime import datetime
import falcon
from api.db import CONNECTION
from api.utils import validate_date, CORSMiddleware

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
            select = "SELECT sum(SANCTION), sum(ADDITION), sum(SAVING), sum(REVISED)"
            from_str = "FROM himachal_budget_allocation_expenditure"
            where = "WHERE date BETWEEN '{}' and '{}'".format(start, end)
            groupby = "GROUP BY WEEK(DATE(date))"

            for key, value in payload['filters'].items():
                where += "AND {key} IN ('{value}')".format(key=key, value=value)
            query_string = select + ' ' + from_str + ' ' + where + ' ' + groupby

        query = CONNECTION.execute(query_string)
        data_rows = query.fetchall()
        records = []
        print(query_string)
        for row in data_rows:
            records.append(row.values())
        data_response = json.dumps({'records': records, 'count': len(records)})

        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = data_response

@falcon.before(validate_date)
class DetailExpenditureMonth():
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
                GROUP BY MONTH(DATE(date))
            """
        else:
            select = "SELECT sum(SANCTION), sum(ADDITION), sum(SAVING), sum(REVISED)"
            from_str = "FROM himachal_budget_allocation_expenditure"
            where = "WHERE date BETWEEN '{}' and '{}'".format(start, end)
            groupby = "GROUP BY MONTH(DATE(date))"

            for key, value in payload['filters'].items():
                where += "AND {key} IN ('{value}')".format(key=key, value=value)
            query_string = select + ' ' + from_str + ' ' + where + ' ' + groupby

        query = CONNECTION.execute(query_string)
        data_rows = query.fetchall()
        records = []
        print(query_string)
        for row in data_rows:
            records.append(row.values())
        data_response = json.dumps({'records': records, 'count': len(records)})

        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = data_response

@falcon.before(validate_date)
class TreasuryExpenditureMonth():
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
                SELECT sum(BILLS), sum(GROSS), sum(AGDED), sum(NETPAYMENT)
                FROM himachal_pradesh_district_spending_data
                WHERE date BETWEEN '{}' and '{}'
                GROUP BY MONTH(DATE(TRANSDATE))
            """
        else:
            select = "SELECT sum(BILLS), sum(GROSS), sum(AGDED), sum(NETPAYMENT)"
            from_str = "FROM himachal_pradesh_district_spending_data"
            where = "WHERE TRANSDATE BETWEEN '{}' and '{}'".format(start, end)
            groupby = "GROUP BY MONTH(DATE(TRANSDATE))"

            for key, value in payload['filters'].items():
                where += "AND {key} IN ('{value}')".format(key=key, value=value)
            query_string = select + ' ' + from_str + ' ' + where + ' ' + groupby

        query = CONNECTION.execute(query_string)
        data_rows = query.fetchall()
        records = []
        print(query_string)
        for row in data_rows:
            records.append(row.values())
        data_response = json.dumps({'records': records, 'count': len(records)})

        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = data_response

@falcon.before(validate_date)
class TreasuryExpenditureWeek():
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
                SELECT sum(BILLS), sum(GROSS), sum(AGDED), sum(NETPAYMENT)
                FROM himachal_pradesh_district_spending_data
                WHERE date BETWEEN '{}' and '{}'
                GROUP BY WEEK(DATE(TRANSDATE))
            """
        else:
            select = "SELECT sum(BILLS), sum(GROSS), sum(AGDED), sum(NETPAYMENT)"
            from_str = "FROM himachal_pradesh_district_spending_data"
            where = "WHERE TRANSDATE BETWEEN '{}' and '{}'".format(start, end)
            groupby = "GROUP BY WEEK(DATE(TRANSDATE))"

            for key, value in payload['filters'].items():
                where += "AND {key} IN ('{value}')".format(key=key, value=value)
            query_string = select + ' ' + from_str + ' ' + where + ' ' + groupby

        query = CONNECTION.execute(query_string)
        data_rows = query.fetchall()
        records = []
        print(query_string)
        for row in data_rows:
            records.append(row.values())
        data_response = json.dumps({'records': records, 'count': len(records)})

        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = data_response

class DetailAccountHeads():
    '''
    This API will give permutations and combinations of all account heads
    '''
    def on_get(self, req, resp):
        '''
        Method for getting Permutations Combinations of account heads
        '''
        query_string = "select demand,major,sub_major,minor,sub_minor, budget, voted_charged, plan_nonplan, SOE from himachal_budget_allocation_expenditure GROUP BY demand, major, sub_major ,minor, sub_minor, budget, voted_charged, plan_nonplan, SOE"  # pylint: disable=line-too-long
        query = CONNECTION.execute(query_string)
        data_rows = query.fetchall()
        records = []


        for row in data_rows:
            records.append(row.values())

        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = json.dumps({'records':records, 'count': len(records)})

class DetailAccountHeadsTest():
    '''
    This API will give permutations and combinations of all account heads
    '''
    def on_get(self, req, resp):
        '''
        Method for getting Permutations Combinations of account heads
        '''
        query_string = "select demand,major,sub_major,minor,sub_minor, budget, voted_charged, plan_nonplan, SOE from himachal_budget_allocation_expenditure GROUP BY demand, major, sub_major ,minor, sub_minor, budget, voted_charged, plan_nonplan, SOE"  # pylint: disable=line-too-long
        query = CONNECTION.execute(query_string)
        data_rows = query.fetchall()
        records = []
        for row in data_rows:
            records.append(row.values())        

        dict_hp = {}

        for rows in records:
            current_level = dict_hp
            for acc_heads in rows:
                if acc_heads not in current_level:
                    current_level[acc_heads] = {}
                current_level = current_level[acc_heads]

        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = json.dumps({'records':dict_hp})

class UniqueAccountHeads():
    '''
    This API will give permutations and combinations of all account heads
    '''
    def on_get(self, req, resp):
        '''
        Method for getting Permutations Combinations of account heads
        '''
        query_string = "SELECT `COLUMN_NAME`  FROM `INFORMATION_SCHEMA`.`COLUMNS`  WHERE `TABLE_SCHEMA`='himachal_pradesh_data' AND `TABLE_NAME`='himachal_budget_allocation_expenditure'"  # pylint: disable=line-too-long
        get_column_names = CONNECTION.execute(query_string)
        column_names = get_column_names.fetchall()
        column_names_list  =  [row.values() for row in column_names]     
        target_index = column_names_list.index(['SOE'])
        list_acc_heads = column_names_list[1:target_index+1]
      
        dict_unique_acc_heads = {}
        for acc_heads in list_acc_heads:
            query_select = "select distinct {} from himachal_budget_allocation_expenditure".format(acc_heads[0])
            query_unique_acc_heads = CONNECTION.execute(query_select)
            unique_acc_heads_value = query_unique_acc_heads.fetchall()
            unique_acc_heads_value_list =  [row_acc.values() for row_acc in unique_acc_heads_value] 
            unique_acc_heads_value_list = [acc_heads for acc_heads_value in unique_acc_heads_value_list for acc_heads in acc_heads_value]
            dict_unique_acc_heads[acc_heads[0]] = unique_acc_heads_value_list
        
        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = json.dumps(dict_unique_acc_heads)

class TreasuryAccountHeads():
    '''
    This API will give permutations and combinations of all account heads
    '''
    def on_get(self, req, resp):
        '''
        Method for getting Permutations Combinations of account heads
        '''
        query_string = "select District, Treasury_Code, Treasury, DDO_Code, DDO_Desc,demand,demand_desc,major,major_desc,sub_major,sub_major_desc,minor,minor_desc,sub_minor,sub_major_desc, budget, voted_charged, plan_nonplan, SOE, SOE_description from himachal_pradesh_district_spending_data GROUP BY District, Treasury_Code, Treasury, DDO_Code, DDO_Desc,demand,demand_desc,major,major_desc,sub_major,sub_major_desc,minor,minor_desc,sub_minor,sub_major_desc, budget, voted_charged, plan_nonplan, SOE, SOE_description"  # pylint: disable=line-too-long
        query = CONNECTION.execute(query_string)
        data_rows = query.fetchall()
        records = []
        for row in data_rows:
            records.append(row.values())
        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = json.dumps({'records':records, 'count': len(records)})