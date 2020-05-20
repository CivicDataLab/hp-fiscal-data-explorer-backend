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
class SchemesVisType():
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

    
        select = "SELECT District,sum(GROSS), sum(AGDED), sum(BTDED), sum(NETPAYMENT)"
        from_str = "FROM himachal_budget_schemes_data"
        where = "WHERE TRANSDATE BETWEEN '{}' and '{}'".format(start, end)
        groupby = "GROUP BY District, {}(DATE(TRANSDATE))".format(vis_range)


        for key, value in payload['filters'].items():
            where += "AND {key} IN ({value})".format(key=key, value=value)
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


class SchemesAccountHeads():
    '''
    This API will give permutations and combinations of all account heads
    '''
    def on_get(self, req, resp):
        '''
        Method for getting Permutations Combinations of account heads
        '''
        params = req.params
        list_of_keys = [ k for k in params.keys() ]
        select = "SELECT schemes, Type, District,Treasury_Code,Treasury, DDO_Code, DDO_Desc, demand, demand_desc, major, major_desc, sub_major, sub_major_desc, minor, minor_desc, sub_minor, sub_minor_desc,budget, voted_charged, plan_nonplan, SOE, SOE_description"
        from_str = " FROM himachal_budget_schemes_data"
        where = "where "
        groupby = "GROUP BY schemes, Type, District, Treasury_Code,Treasury, DDO_Code, DDO_Desc,demand, demand_desc, major, major_desc, sub_major, sub_major_desc, minor, minor_desc, sub_minor, sub_minor_desc,budget, voted_charged,plan_nonplan, SOE, SOE_description"
        
        for key, value in params.items():
            where += "{key} IN ({value}) AND ".format(key=key, value=value)
        query_string = select + ' ' + from_str + ' ' + where[:len(where)-4] + ' ' + groupby
        print(query_string)

        query = CONNECTION.execute(query_string)
        data_rows = query.fetchall()
        records = []

        records = [row.values() for row in data_rows]     
        records_with_desc = [] 

        for i in range(len(records)):
            records_list = []
            records_list.append(records[i][0:3])
            
            for j in range(3,16,2):
                records_list.append(['-'.join(records[i][j:j+2])])
            records_list.append(records[i][17:20])
            
            records_list.append(['-'.join(records[i][20:22])])
           
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

class UniqueAccountHeadsSchemes():
    '''
    This API will give permutations and combinations of all account heads
    '''
    def on_get(self, req, resp):
        '''
        Method for getting Permutations Combinations of account heads
        '''
        query_string = "SELECT `COLUMN_NAME`  FROM `INFORMATION_SCHEMA`.`COLUMNS`  WHERE `TABLE_SCHEMA`='himachal_pradesh_expenditure_data' AND `TABLE_NAME`='himachal_budget_schemes_data'"  # pylint: disable=line-too-long
        get_column_names = CONNECTION.execute(query_string)
        column_names = get_column_names.fetchall()
        
        column_names_list  =  [row.values() for row in column_names]     
        
        list_acc_heads_with_desc =column_names_list[4:18] + column_names_list[21:23]
        list_acc_heads_without_desc = []
        list_acc_heads_without_desc = [acc_head[0] for acc_head in column_names_list if acc_head not in list_acc_heads_with_desc]
        list_acc_heads_without_desc.pop(0)
        print(list_acc_heads_without_desc)
        #list_acc_heads_without_desc = [acc_heads for acc_heads_value in list_acc_heads_without_desc  for acc_heads in acc_heads_value]
        
        dict_unique_acc_heads = {}
        
    
        for acc_heads_index in range(0,15,2):
            query_select = "select distinct concat_ws('-',{},{}) from himachal_budget_schemes_data".format(list_acc_heads_with_desc[acc_heads_index][0],list_acc_heads_with_desc[acc_heads_index+1][0])
            print(query_select)
            query_unique_acc_heads = CONNECTION.execute(query_select)
            unique_acc_heads_value = query_unique_acc_heads.fetchall()
            unique_acc_heads_value_list =  [row_acc.values() for row_acc in unique_acc_heads_value] 
            unique_acc_heads_value_list = [acc_heads for acc_heads_value in unique_acc_heads_value_list for acc_heads in acc_heads_value]
            dict_unique_acc_heads[list_acc_heads_with_desc[acc_heads_index][0]] = unique_acc_heads_value_list

        for acc_heads_index in range(0,6):
            query_select = "select distinct {} from himachal_budget_schemes_data".format(list_acc_heads_without_desc[acc_heads_index])
            print(query_select)
            query_unique_acc_heads = CONNECTION.execute(query_select)
            unique_acc_heads_value = query_unique_acc_heads.fetchall()
            unique_acc_heads_value_list =  [row_acc.values() for row_acc in unique_acc_heads_value] 
            unique_acc_heads_value_list = [acc_heads for acc_heads_value in unique_acc_heads_value_list for acc_heads in acc_heads_value]
            dict_unique_acc_heads[list_acc_heads_without_desc[acc_heads_index]] = unique_acc_heads_value_list

        resp.status = falcon.HTTP_200  #pylint: disable=no-member
        resp.body = json.dumps(dict_unique_acc_heads)

