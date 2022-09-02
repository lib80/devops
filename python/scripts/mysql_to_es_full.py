#!/usr/bin/env python3
# 本脚本用于同步mysql到elasticsearch（全量）
# author: libin
import datetime
import pymysql
import pandas
import elasticsearch

items_to_deal = [
    {
        'name': 'xxx',
        'primary_key': 'xxx',
        'sql': "xxx",
        'index': 'xxx',
        'mappings': {}
    },
    {
        'name': 'xxx',
        'primary_key': 'xxx',
        'sql': "xxx",
        'index': 'xxx',
        'mappings': {}
    }
]

my_info = {
    'user': 'xxx',
    'password': 'xxx',
    'database': 'xxx',
    'unix_socket': '/tmp/mysql.sock'
}

my_conn = pymysql.connect(**my_info)
es_conn = elasticsearch.Elasticsearch(['http://localhost:9200'], sniff_on_start=True, sniff_on_connection_fail=True, sniffer_timeout=60)


def deal(item: dict):
    index = item['index']
    if es_conn.indices.exists(index=index):
        es_conn.indices.delete(index=index)
    es_conn.indices.create(index=index, mappings=item['mappings'])

    data = pandas.read_sql(sql=item['sql'], con=my_conn, chunksize=1000)
    for chunk in data:
        for _, row in chunk.iterrows():
            row = dict(row)
            for k, v in row.items():
                if pandas.isna(v) or pandas.isnull(v):
                    row[k] = None
                if isinstance(row[k], datetime.datetime):
                    row[k] = v.strftime('%Y-%m-%d %H:%M:%S')
            if item.get('name') == 'famous':
                if row.get('job'):
                    row['job'] = row['job'].decode('utf-8')
                if row.get('resume'):
                    row['resume'] = row['resume'].decode('utf-8')
            es_conn.index(index=index, id=row.get(item.get('primary_key')), document=row)


for item in items_to_deal:
    deal(item)

es_conn.close()
my_conn.close()
