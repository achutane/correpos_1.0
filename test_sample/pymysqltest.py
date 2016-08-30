# モジュール読み込み
import pymysql.cursors
# MySQLに接続する

if __name__ == "__main__":
    
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             db='testdb',
                             charset='utf8',
                             # cursorclassを指定することで
                             # Select結果をtupleではなくdictionaryで受け取れる
                             cursorclass=pymysql.cursors.DictCursor)
    # SQLを実行する
    with connection.cursor() as cursor:
        sql = "SELECT * FROM Test"
        cursor.execute(sql)
    
        # Select結果を取り出す
        results = cursor.fetchall()
        for r in results:
            print(r)
            # => {'name': 'Cookie', 'id': 3}
                                 
connection.close()