import pymysql.cursors
import threading
from logic.serial_bt import *
import pandas as pd

# Connect to the database
connection = pymysql.connect(host='10.10.10.110',
                             user='root',
                             password='123',
                             database='projectdb',
                             cursorclass=pymysql.cursors.DictCursor)


def init():
    clear_table()

    with connection.cursor() as cursor:
        cursor.execute("ALTER TABLE dht11tbl AUTO_INCREMENT = 1")  # idx 값 0으로 초기화
        connection.commit()

def save_csv():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dht11tbl")
        rows = cursor.fetchall()

        df = pd.DataFrame(rows)
        df.to_csv(f'./csv_data/data_{time.strftime("%Y%m%d_%H%M%S")}.csv', index=False)
        print("csv 저장 완료")

def clear_table():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM dht11tbl")
        connection.commit()
        print("테이블 내용이 삭제되었습니다.")


def save_sensor_data():
    count = 0
    init()
    while True:
        time.sleep(1)
        dht = return_receDATA()

        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO dht11tbl (sensor_id, temperature, humidity) VALUES (%s, %s, %s)"
                cursor.execute(sql, (1, dht[0], dht[1]))

                sql = "INSERT INTO dht11tbl (sensor_id, temperature, humidity) VALUES (%s, %s, %s)"
                cursor.execute(sql, (2, dht[2], dht[3]))
            connection.commit()
            count += 2

            if count % 20 == 0:
                save_csv()
                clear_table()
                count = 0


        except Exception as e:
            print(f"DB 저장 중 에러 발생: {e}")

        

# 스레드 실행 함수
def db_thread_start():
    time.sleep(5)
    db_thread = threading.Thread(target=save_sensor_data)
    db_thread.start()