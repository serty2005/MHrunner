import requests
import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Функция для получения данных
def fetch_data(meta_class, params):
    url = f'{os.getenv("BASE_URL")}/sd/services/rest/find/{meta_class}?accessKey={os.getenv("ACCESS_KEY")}&attrs={params}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Функция для создания таблицы SQLite
def create_table(conn, table_name, columns):
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns}
        )
    ''')
    conn.commit()

# Функция для проверки и форматирования данных
def validate_company_data(item):
    # Преобразование lastModifiedDate в datetime
    last_modified_date = item.get('lastModifiedDate', '')
    if last_modified_date is not None and isinstance(last_modified_date, str):
        try:
            item['lastModifiedDate'] = datetime.strptime(last_modified_date, '%Y.%m.%d %H:%M:%S')
        except ValueError:
            return None

    return item

# Функция для вставки данных в таблицу
def insert_data(conn, table_name, columns, data, validate_func):
    cursor = conn.cursor()
    for item in data:
        item = validate_func(item)
        if item is not None:
            cursor.execute(f'''
                INSERT OR REPLACE INTO {table_name} ({columns})
                VALUES (?, ?, ?, ?)
            ''', (
                item.get('UUID'),
                item.get('lastModifiedDate'),
                item.get('adress'),
                item.get('title')
            ))
    conn.commit()

# Основная функция
def main():
    # Получение данных для Companies
    companies_data = fetch_data(os.getenv("COMPANIES_METACLASS"), os.getenv("COMPANIES_PARAMS"))
    
    # Подключение к базе данных
    conn = sqlite3.connect('servers.db')
    
    # Создание таблицы Companies
    create_table(conn, 'Companies', '''
        UUID TEXT PRIMARY KEY,
        lastModifiedDate DATETIME,
        adress TEXT,
        title TEXT
    ''')
    
    # Вставка данных в таблицу Companies
    insert_data(conn, 'Companies', 'UUID, lastModifiedDate, adress, title', companies_data, validate_company_data)
    
    # Закрытие соединения
    conn.close()

if __name__ == '__main__':
    main()
