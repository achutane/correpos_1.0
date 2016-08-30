# -*- coding: utf-8 -*-
#import MySQLdb
import mysql.connector

if __name__ == "__main__":


    #接続情報
    dbh = mysql.connector.connect(
            host='localhost',
            port='3306',
            db='testdb',
            user='root',
            password='password',
            charset='utf8'
        )
    
    #カーソル取得
    stmt = dbh.cursor(buffered=True)
    
    #SQL
    sql = "select * from Test"
    
    #実行
    stmt.execute(sql)
    
    #取得
    rows = stmt.fetchall()
    
    #ループ
    for row in rows:
        print(row[1])
    
    #掃除
    stmt.close()
    dbh.close()