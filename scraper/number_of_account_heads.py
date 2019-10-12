#!/usr/bin/env python
import pandas as pd
import numpy as np
budget_hoa = pd.read_csv('../datasets/hoa_budget_expenditure/March/budget_expenditures_20190301.csv')
budget_hoa.head()
budget_hoa.columns = ['DM_MAJ_SM_MIN_SMN_BUD_VC_PN_SOE', 'SANCTION', 'ADDITION','SAVING','REVISE0D']
budget_hoa = budget_hoa[~budget_hoa.DM_MAJ_SM_MIN_SMN_BUD_VC_PN_SOE.str.contains("Grand", na=False)]
budget_hoa_splited = budget_hoa.DM_MAJ_SM_MIN_SMN_BUD_VC_PN_SOE.str.split('-', expand = True, n = 9)
budget_hoa_splited.columns = ['demand', 'major','sub_major','minor', 'sub_minor','budget','voted_charged','plan_nonplan','SOE','SOE_description']
budget_hoa[['demand','major','sub_major','minor', 'sub_minor','budget','voted_charged','plan_nonplan','SOE','SOE_description']] = budget_hoa_splited[['demand','major','sub_major', 'minor', 'sub_minor','budget','voted_charged','plan_nonplan','SOE','SOE_description']]
budget_hoa.nunique()
