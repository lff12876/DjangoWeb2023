import csv
from pandas.core.frame import DataFrame
import pandas as pd
from sqlalchemy import create_engine

tmp_lst = []


with open('../server_data/jy20230525_202305272128.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        tmp_lst.append(row)
df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])

if __name__ == '__main__':
    #print(df)
    #engine = create_engine("mysql+mysqlconnector://root:adminroot933!17@localhost:3306/djangoweb?charset=utf8")
    engine = create_engine("mysql+mysqlconnector://test:test;123@182.92.194.9:3306/djangoweb?charset=utf8")
    con = engine.connect()

    df.to_sql(name="oauth_stockdata", con=engine, index=False, if_exists="append")

    con.close()


