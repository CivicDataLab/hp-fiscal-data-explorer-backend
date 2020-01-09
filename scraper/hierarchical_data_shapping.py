#!/usr/bin/env python
# coding: utf-8
import pandas as pd
budget_hoa = pd.read_csv('../datasets/hoa_budget_expenditure/March/budget_expenditures_20190301.csv')
budget_hoa.columns = ['DM_MAJ_SM_MIN_SMN_BUD_VC_PN_SOE', 'SANCTION', 'ADDITION','SAVING','REVISED']
budget_hoa = budget_hoa[~budget_hoa.DM_MAJ_SM_MIN_SMN_BUD_VC_PN_SOE.str.contains("Grand", na=False)]
budget_hoa_splited = budget_hoa.DM_MAJ_SM_MIN_SMN_BUD_VC_PN_SOE.str.split('-', expand = True, n = 9)
budget_hoa_splited.columns = ['demand', 'major','sub_major','minor', 'sub_minor','budget','voted_charged','plan_nonplan','SOE','SOE_description']
budget_hoa[['demand','major','sub_major','minor', 'sub_minor','budget','voted_charged','plan_nonplan','SOE','SOE_description']] = budget_hoa_splited[['demand','major','sub_major', 'minor', 'sub_minor','budget','voted_charged','plan_nonplan','SOE','SOE_description']]
budget_hoa = budget_hoa.drop('DM_MAJ_SM_MIN_SMN_BUD_VC_PN_SOE', axis = 1)
budget_hoa_final = budget_hoa[['demand','major','sub_major','minor', 'sub_minor','budget','voted_charged','plan_nonplan','SOE','SOE_description','SANCTION','ADDITION','SAVING','REVISED']]
budget_hoa.columns
number_of_major_heads = budget_hoa[['demand','major']].groupby(['demand']).agg(['count','nunique'])
number_of_major_heads.to_csv('../datasets/Number of heads/number_of_major_heads.csv')
number_of_major_heads.max()
number_of_major_heads.min()
number_of_sub_major_heads = budget_hoa[['demand','major','sub_major']].groupby(['demand','major']).agg(['count','nunique'])
number_of_sub_major_heads.to_csv('../datasets/Number of heads/number_of_sub_major_heads.csv')
number_of_sub_major_heads.max()
number_of_sub_major_heads.max()
number_of_minor_heads = budget_hoa[['demand','major','sub_major','minor']].groupby(['demand','major','sub_major']).agg(['count','nunique'])
number_of_minor_heads.to_csv('../datasets/Number of heads/number_of_minor_heads.csv')
number_of_minor_heads.max()
number_of_minor_heads.min()
number_of_sub_minor_heads = budget_hoa[['demand','major','sub_major','minor', 'sub_minor']].groupby(['demand','major','sub_major', 'minor']).agg(['count','nunique'])
number_of_sub_minor_heads.to_csv('../datasets/Number of heads/number_of_sub_minor_heads.csv')
number_of_sub_minor_heads.max()
number_of_sub_minor_heads.min()
number_of_budget_heads = budget_hoa[['demand','major','sub_major','minor','sub_minor','budget']].groupby(['demand','major','sub_major','minor','sub_minor']).agg(['count','nunique'])
number_of_budget_heads.to_csv('../datasets/Number of heads/number_of_budget_heads.csv')
number_of_budget_heads.max()
number_of_budget_heads.min()
number_of_soe_heads = budget_hoa[['demand','major','sub_major','minor','sub_minor','budget', 'SOE']].groupby(['demand','major','sub_major','minor','sub_minor','budget']).agg(['count','nunique'])
number_of_soe_heads.to_csv('../datasets/Number of heads/number_of_soe_heads.csv')
number_of_soe_heads.max()
number_of_soe_heads.min()

