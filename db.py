import mysql.connector
import os
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def get_employee_id(name):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT id FROM employees WHERE name = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result[0]
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Ошибка базы данных: {err}")
        return None

def add_employee(name, department, role, hire_date):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO employees (name, department, role, hire_date)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (name, department, role, hire_date))
    conn.commit()
    cursor.close()
    conn.close()


def start_work_session(employee_id):
  try:
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO work_sessions (employee_id, start_time) VALUES (%s, NOW())"
    cursor.execute(query, (employee_id,))
    conn.commit()
    cursor.close()
    conn.close()
  except mysql.connector.Error as err:
      print(f"Ошибка базы данных: {err}")

def end_work_session(employee_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE work_sessions SET end_time = NOW() WHERE employee_id = %s AND end_time IS NULL"
        cursor.execute(query, (employee_id,))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Ошибка базы данных: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
