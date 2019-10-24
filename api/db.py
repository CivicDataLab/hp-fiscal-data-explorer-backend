'''
database connection
'''
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:admin123@localhost/himachal_pradesh_expenditure_data")
connection = engine.connect()