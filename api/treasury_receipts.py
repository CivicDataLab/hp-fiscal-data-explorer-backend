import json
from datetime import datetime
import falcon
import pdb
from api.db import CONNECTION
from api.utils import validate_date, CORSMiddleware, validate_vis_range
import time
import pandas as pd



@falcon.before(validate_date)
@falcon.before(validate_vis_range)
class TreasuryReceiptsVisType():
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
        vis_range = params['range']

        req_body = req.stream.read()
        if req_body:
            payload = json.loads(req_body)
        else:
            payload = {}

    
        select = "SELECT District,sum(NETRECEIPT)"
        from_str = "FROM himachal_pradesh_district_receipts_data"
        where = "WHERE BOOKDATE BETWEEN '{}' and '{}'".format(start, end)
        groupby = "GROUP BY District, {}(DATE(BOOKDATE))".format(vis_range)


        for key, value in payload['filters'].items():
            where += "AND {key} IN ('{value}')".format(key=key, value=value)
        query_string = select + ' ' + from_str + ' ' + where + ' ' + groupby
      
        query = CONNECTION.execute(query_string)
        data_rows = query.fetchall()
        records = []
        
        for row in data_rows:
            records.append(row.values())
        dict_hp = {}

        districts = []
        values = []

        for i in records:
            districts.append(i[0])
            values.append(i[1:])

        dict_hp = {}

        for i in districts:
            dict_hp[i] = []

        for i in range(0,len(districts)):
            dict_hp[districts[i]].append(values[i])

        data_response = json.dumps({'records': dict_hp, 'count': len(records)})

        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = data_response

class TreasuryReceiptsAccountHeads():
    '''
    This API will give permutations and combinations of all account heads
    '''
    def on_get(self, req, resp):
        '''
        Method for getting Permutations Combinations of account heads
        '''
        params = req.params
        list_of_keys = [ k for k in params.keys() ]
        select = "SELECT District,Treasury_Code,Treasury, DDO_Code, DDO_Desc, major_code, major_desc, sub_major_code, minor_code, sub_major_code, sub_minor_desc"
        from_str = " FROM himachal_pradesh_district_receipts_data"
        where = "where "
        groupby = "GROUP BY District, Treasury_Code,Treasury, DDO_Code, DDO_Desc , major_code, major_desc, sub_major_code, minor_code, sub_major_code, sub_minor_desc"
        
        for key, value in params.items():
            where += "{key} IN ({value}) AND ".format(key=key, value=value)
        query_string = select + ' ' + from_str + ' ' + where[:len(where)-4] + ' ' + groupby
       
        query = CONNECTION.execute(query_string)
        data_rows = query.fetchall()
        records = []

        records = [row.values() for row in data_rows]     
        records_with_desc = [] 

        for i in range(len(records)):
            records_list = []
            records_list.append(records[i][0:1])
           
            for j in range(1,6,2):
                records_list.append(['-'.join(records[i][j:j+2])])
            records_list.append(records[i][7:9])
            
            records_list.append(['-'.join(records[i][9:12])])
           
            records_list = [acc_heads for acc_heads_value in records_list for acc_heads in acc_heads_value]
            
            records_with_desc.append(records_list)

           

        dict_hp = {}

        for rows in records_with_desc:
            current_level = dict_hp
            for acc_heads in rows:
                if acc_heads not in current_level:
                    current_level[acc_heads] = {}
                current_level = current_level[acc_heads]
        
        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = json.dumps({'records':dict_hp})  
