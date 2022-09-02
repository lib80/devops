#!/usr/bin/env python3
# 本脚本用于同步mysql到elasticsearch（增量）: 从canal-server获取数据库变更，解析后写入es
# author: libin

import time
import logging
from logging.handlers import TimedRotatingFileHandler
import binascii
import elasticsearch
from Crypto.Cipher import AES
from canal.client import Client
from canal.protocol import EntryProtocol_pb2
from canal.protocol import CanalProtocol_pb2

ES_HOST = 'xxx'
CANAL_HOST = 'xxx'
CANAL_PORT = 'xxx'
CANAL_USER = b'xxx'
CANAL_PASSWORD = b'xxx'
LOG_FILE = 'xxx'
AES_KEY = b'xxx'

filter_tables = {
    'xxx.xxx': {'xxx': 'xxx',
                      'filter_fields': ['xxx', 'xxx', 'xxx']},
    'xxx.xxx': {'xxx': 'xxx',
                        'filter_fields': ['xxx', 'xxx', 'xxx']},
}
es_conn = elasticsearch.Elasticsearch([ES_HOST], sniff_on_start=True, sniff_on_connection_fail=True,
                                      sniffer_timeout=60)
# 连接canal-server
client = Client()
client.connect(host=CANAL_HOST, port=CANAL_PORT)
client.check_valid(username=CANAL_USER, password=CANAL_PASSWORD)
client.subscribe(client_id=b'1001', destination=b'example', filter=','.join(filter_tables.keys()).encode())

logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
log_file_handler = TimedRotatingFileHandler(filename=LOG_FILE, when='D', interval=1, backupCount=15)
log_file_handler.suffix = '%Y-%m-%d.log'
log_file_handler.setFormatter(formatter)
logger.addHandler(log_file_handler)
logger.setLevel(logging.WARNING)

aes = AES.new(key=AES_KEY, mode=AES.MODE_ECB)


def aes_hex_decrypt(text):
    if text:
        # 去掉末尾乱码
        res = aes.decrypt(binascii.a2b_hex(text)).decode('utf-8')
        padding_len = ord(res[len(res) - 1])
        return res[0:-padding_len]
    else:
        return text


while True:
    message = client.get(100)
    entries = message['entries']
    for entry in entries:
        entry_type = entry.entryType
        if entry_type in [EntryProtocol_pb2.EntryType.TRANSACTIONBEGIN, EntryProtocol_pb2.EntryType.TRANSACTIONEND]:
            continue
        row_change = EntryProtocol_pb2.RowChange()
        row_change.MergeFromString(entry.storeValue)
        event_type = row_change.eventType
        header = entry.header
        database = header.schemaName
        table = header.tableName
        event_type = header.eventType

        table_extra_info = filter_tables.get(f'{database}.{table}')
        if not table_extra_info:
            continue
        index = table_extra_info['index']
        filter_fields = table_extra_info['filter_fields']

        for row in row_change.rowDatas:
            # format_data = dict()
            if event_type == EntryProtocol_pb2.EventType.DELETE:
                for column in row.beforeColumns:
                    # format_data['before'][column.name] = column.value
                    if column.isKey:
                        try:
                            es_conn.delete(index=index, id=column.value)
                        except Exception as e:
                            logger.error(e)
                        finally:
                            break
            else:
                document_id = None
                document_body = {}
                for column in row.afterColumns:
                    # format_data['after'][column.name] = column.value

                    if column.isKey:
                        document_id = column.value
                    if column.name in filter_fields:
                        if not column.value:
                            document_body[column.name] = None  # canal将字段值都转成了字符串类型，向es插入空串时可能报类型错误，需要转为None
                        else:
                            document_body[column.name] = column.value
                if table == 't_famous':
                    document_body['job'] = aes_hex_decrypt(document_body['job'])
                    document_body['resume'] = aes_hex_decrypt(document_body['resume'])
                if event_type == EntryProtocol_pb2.EventType.INSERT:
                    try:
                        es_conn.index(index=index, id=document_id, document=document_body)
                    except Exception as e:
                        logger.error(e)
                else:
                    try:
                        es_conn.update(index=index, id=document_id, doc=document_body)
                    except Exception as e:
                        logger.error(e)
    time.sleep(1)

client.disconnect()
