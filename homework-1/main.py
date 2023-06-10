"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import psycopg2
"""
Созданы переменные для хранения пути к файлу
"""
file_customers = 'north_data/customers_data.csv'
file_employees = 'north_data/employees_data.csv'
file_orders = 'north_data/orders_data.csv'


def reader(file):
    """
    Функция для чтения файлов формата .csv
    принимающая на вход файл и возвращающая список с данными из файла
    """
    all_items = []
    with open(file, newline='') as file_csv:
        data = csv.DictReader(file_csv)
        for item in data:
            all_items.append(item)
        return all_items


"""
Скрипт для таблиц данными из файлов с использованием контекстного менеджера with
"""
with psycopg2.connect(
    host='localhost',
    database='north',
    user='postgres',
    password=''
) as conn:
    with conn.cursor() as cur:
        employees = reader(file_employees)
        for i in employees:
            cur.execute('INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)', (
                i['employee_id'],
                i['first_name'],
                i['last_name'],
                i['title'],
                i['birth_date'],
                i['notes']))
    with conn.cursor() as cur:
        customers = reader(file_customers)
        for i in customers:
            cur.execute('INSERT INTO customers VALUES (%s, %s, %s)', (
                i['customer_id'],
                i['company_name'],
                i['contact_name'],))
    with conn.cursor() as cur:
        orders = reader(file_orders)
        for i in orders:
            cur.execute('INSERT INTO orders VALUES (%s, %s, %s, %s, %s)', (
                i['order_id'],
                i['customer_id'],
                i['employee_id'],
                i['order_date'],
                i['ship_city']))
conn.close()
