import requests
import sqlite3, os, re
from dotenv import load_dotenv


# Загрузка переменных окружения
load_dotenv()

# Функция для получения данных
def fetch_data():
    url = f'{os.getenv("BASE_URL")}/sd/services/rest/find/{os.getenv("SERVERS_METACLASS")}?accessKey={os.getenv("ACCESS_KEY")}&attrs={os.getenv("SERVERS_PARAMS")}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def validate_data(item):
    unique_id = item.get('UniqueID', '')
    if unique_id is None or not isinstance(unique_id, str) or not re.match(r'^\d{3}-\d{3}-\d{3}$', unique_id):
        return None
    
    cabinet_link = item.get('CabinetLink', '')
    if cabinet_link is not None or isinstance(cabinet_link, str):
        if cabinet_link.startswith('https://partners.iiko.ru/ru/cabinet/') or cabinet_link.startswith('https://partners.iiko.ru/en/cabinet/'):
            cabinet_link = re.sub(r'https://partners\.iiko\.ru/(ru|en)/cabinet/', 'https://partners.iiko.ru/v2/ru/cabinet/', cabinet_link)
        item['CabinetLink'] = cabinet_link
    

    return item

# Функция для создания таблицы SQLite
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servers (
            UUID TEXT PRIMARY KEY,
            Teamviewer TEXT,
            UniqueID TEXT,
            IP TEXT,
            CabinetLink TEXT,
            title TEXT,
            AnyDesk TEXT,
            DeviceName TEXT,
            owner TEXT
        )
    ''')
    conn.commit()

# Функция для вставки данных в таблицу
def insert_data(conn, data):
    cursor = conn.cursor()
    for item in data:
        item = validate_data(item)
        if item is not None:
            owner_uuid = item.get('owner', {}).get('UUID') if item.get('owner') else ''
            cursor.execute('''
                INSERT OR REPLACE INTO servers (UUID, Teamviewer, UniqueID, IP, CabinetLink, title, AnyDesk, DeviceName, owner)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.get('UUID'),
                item.get('Teamviewer'),
                item.get('UniqueID'),
                item.get('IP'),
                item.get('CabinetLink'),
                item.get('title'),
                item.get('AnyDesk'),
                item.get('DeviceName'),
                owner_uuid
            ))
    conn.commit()

# Основная функция
def main():
    data = fetch_data()
    conn = sqlite3.connect('servers.db')
    create_table(conn)
    insert_data(conn, data)
    conn.close()

if __name__ == '__main__':
    main()
