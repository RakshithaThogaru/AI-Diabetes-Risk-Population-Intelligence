import getpass
import mysql.connector
from mysql.connector import Error

try:
    username = input("Enter your MySQL username (usually root): ")
    password = getpass.getpass("Enter your MySQL password: ")

    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user=username,
        password=password,
        database="ai_diabetes_db"
    )

    if connection.is_connected():
        print("\nSUCCESS: Python connected to MySQL!")

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM ai_diabetes_db.diabetes_raw"
        )
        raw_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM ai_diabetes_db.diabetes_model_ready"
        )
        processed_count = cursor.fetchone()[0]

        print("Raw records:", raw_count)
        print("Processed records:", processed_count)

        cursor.close()
        connection.close()
        print("MySQL connection closed successfully.")

except Error as error:
    print("\nConnection failed:", error)
    print("Check your MySQL username, password, host and port.")