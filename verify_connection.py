import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'Qwert@123'),
    'database': os.getenv('MYSQL_DATABASE', 'resume'),
    'auth_plugin': 'mysql_native_password'
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print("Connection successful with mysql_native_password authentication!")
    
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("Tables in database: " + str(tables))
    
    conn.close()
    print("All tests passed!")
    
except mysql.connector.Error as err:
    print("Error: " + str(err))
except Exception as e:
    print("Error: " + str(e))
    import traceback
    traceback.print_exc()
