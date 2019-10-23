'''
database connection
'''
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:shreya@localhost/himachal")
connection = engine.connect()