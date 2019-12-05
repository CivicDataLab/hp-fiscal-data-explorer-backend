'''
receipts data endpoints
'''
import json
from datetime import datetime
import falcon
from api.db import CONNECTION
from api.utils import validate_date, CORSMiddleware


@falcon.before(validate_date)
class DetailReceiptsWeek():
    '''
    detail receipts endpoint
    '''
    def on_post(self, req, resp):
        '''
        Receipts data endpoint
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
                SELECT sum(Total_Receipt)
                FROM himachal_budget_receipts_data
                WHERE date BETWEEN '{}' and '{}'
                GROUP BY WEEK(DATE(date))
            """
        else:
            select = "SELECT sum(Total_Receipt)"
            from_str = "FROM himachal_budget_receipts_data"
            where = "WHERE date BETWEEN '{}' and '{}'".format(start, end)
            groupby = "GROUP BY WEEK(DATE(date))"

            for key, value in payload['filters'].items():
                where += "AND {key} IN ({value})".format(key=key, value=value)
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

class ReceiptsAccountHeads():
    '''
    This API will give permutations and combinations of all account heads
    '''
    def on_get(self, req, resp):
        '''
        Method for getting Permutations Combinations of account heads
        '''
        query_string = "select major,sub_major,minor,sub_minor from himachal_budget_receipts_data GROUP BY major, sub_major ,minor, sub_minor"  # pylint: disable=line-too-long
        query = CONNECTION.execute(query_string)
        data_rows = query.fetchall()
        records = []
        for row in data_rows:
            records.append(row.values())
        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = json.dumps({'records':records, 'count': len(records)})
        