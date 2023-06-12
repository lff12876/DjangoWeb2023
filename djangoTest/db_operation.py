import csv
from pandas.core.frame import DataFrame
import pandas as pd
from sqlalchemy import create_engine

tmp_lst = []
#此文件仅用于开发过程中向本地或远程服务器推送数据

with open('../server_data/jy20230525_202305272128.csv', 'r') as f:#本地csv文件
    reader = csv.reader(f)
    for row in reader:
        tmp_lst.append(row)
df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])#读取成DataFrame

if __name__ == '__main__':
    engine = create_engine("mysql+mysqlconnector://username:password@address:3306/dbname?charset=utf8")
    con = engine.connect()

    df.to_sql(name="oauth_stockdata", con=engine, index=False, if_exists="append")#这里的name是数据库表名

    con.close()


