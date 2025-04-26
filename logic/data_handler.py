import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='10.10.10.110',
                             user='user',
                             password='123',
                             database='projectdb',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # Create a new record
        SQL = "INSERT INTO dht11tbl (sensor_id, temperature, humidity) VALUES (%s, %s, %s)"
        cursor.execute(SQL, (1, 24, 60)) # example sensor_id = 1, Temp = 24, Hum = 60

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        SQL = "SELECT * FROM dht11tbl"
        cursor.execute(SQL)
        result = cursor.fetchone()
        print(result)