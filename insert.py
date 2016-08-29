# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 17:53:33 2016

@author: M Y
"""

# モジュール読み込み
import pymysql.cursors
import time

"""
anacondaで
mysql -u root -p

mysqlで
CREATE DATABASE correpos;
USE correpos;
CREATE TABLE user (
    TIMESTAMP int,
    count int
);
"""

# MySQLに接続する
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password', #MySQLのpassに変更
                             db='correpos', #DATABASEの名前
                             charset='utf8',
                             # cursorclassを指定することで
                             # Select結果をtupleではなくdictionaryで受け取れる
                             cursorclass=pymysql.cursors.DictCursor)

# Insert処理
def Insert(count):
    with connection.cursor() as cursor:
        sql = "INSERT INTO user (TIMESTAMP, count) VALUES (%s, %s)"
        if count>0:
            c=count+1
        else:
            c=0
        r = cursor.execute(sql, (time.time(),c))
        print(r) # -> 1
        # autocommitではないので、明示的にコミットする
        connection.commit()
        
# SQLを実行する
# user(TIMESTANP)
with connection.cursor() as cursor:
    Insert(2)

    
    sql = "SELECT count, TIMESTAMP FROM user WHERE count >= 0"
    cursor.execute(sql)

    # Select結果を取り出す
    results = cursor.fetchall()
    for r in results:
        print(r)
        # => {'name': 'Cookie', 'id': 3}

# MySQLから切断する
connection.close()