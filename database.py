import pandas as pd
import io
from sqlalchemy import create_engine
from datetime import datetime
from polygon import RESTClient
from settings import API_KEY


def init_data():
    df = pd.read_csv('datasets/lvmh.csv')
    last_date = df.iloc[-1]['date']

    client = RESTClient(API_KEY)

    start_date = last_date
    end_date = f'{datetime.now():%Y-%m-%d}'
    companies = [
           "LVMHF",
    ]

    payloads = []

    for company in companies:
           aggs = client.get_aggs(
               company,
               1,
               "day",
               start_date,
               end_date,
           )
           for agg in aggs:
                payloads.append({
                    'date': datetime.fromtimestamp(agg.timestamp / 1000),
                    'symbol': 'MOH.F',
                    'adj_close': agg.vwap,
                    'close': agg.close,
                    'high': agg.high,
                    'low': agg.low,
                    'open': agg.open,
                    'volume': agg.volume,
               })

    dd = pd.DataFrame(payloads)

    df = pd.concat([df, dd]).drop_duplicates('date')

    try:
        engine = create_engine('postgresql://postgres:postgrespw@postgres:5432')
        df.head(0).to_sql('stock', engine, if_exists='replace',
                          index=False)  # drops old table and creates new empty table
        conn = engine.raw_connection()
        cur = conn.cursor()
        output = io.StringIO()
        df.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        cur.copy_from(output, 'stock', null="")  # null values become ''
        conn.commit()
    except Exception as e:
        print(e)
        print("Database not connected successfully")
    return df

