import psycopg2
from psycopg2.extras import RealDictCursor

import time
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Sangita',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection successful")
        break

    except Exception as error:
        print("error:", error)
        time.sleep(2)
