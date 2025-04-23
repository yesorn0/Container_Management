import pymysql.cursors
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

connection = pymysql.connect(
    host='10.10.10.110',
    user='user',
    password='123',
    database='projectdb',
    cursorclass=pymysql.cursors.DictCursor
)
# 데이터 저장하기
def insert_sensor_data():
    try:
        with connection.cursor() as cursor:
            SQL = "INSERT INTO dht11tbl (sensor_id, temperature, humidity) VALUES (%s, %s, %s)" 
            cursor.execute(SQL, (1, 24, 60))
        connection.commit()
    except Exception as e:
        print("데이터 삽입 중 오류:", e)

# 
def get_sensor_data():
    try:
        with connection.cursor() as cursor:
            SQL = "SELECT sensor_id, measured_at, temperature, humidity FROM dht11tbl ORDER BY measured_at"
            cursor.execute(SQL)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print("데이터 조회 중 오류:", e)
        return []
# 그래프 기리기
def plot_sensor_data(data):
    if not data:
        print("데이터가 없습니다.")
        return
    dates = [row['measured_at'] for row in data]
    temperatures = [row['temperature'] for row in data]
    humidities = [row['humidity'] for row in data]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, temperatures, label='온도 (°C)', color='red')
    plt.plot(dates, humidities, label='습도 (%)', color='blue')
    plt.xlabel('시간')
    plt.ylabel('값')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.show()

# 실행
if __name__ == "__main__":
    insert_sensor_data()
    data = get_sensor_data()
    plot_sensor_data(data)
    connection.close()