import requests
import sqlite3
import os
import re
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
def validate_workstation_data(item):
    # Проверка наличия DeviceName
    if not item.get('DeviceName'):
        return None

    # Преобразование lastModifiedDate в datetime
    last_modified_date = item.get('lastModifiedDate', '')
    if last_modified_date is not None and isinstance(last_modified_date, str):
        try:
            item['lastModifiedDate'] = datetime.strptime(last_modified_date, '%Y.%m.%d %H:%M:%S')
        except ValueError:
            return None
        
    # Обработка поля Teamviewer
    teamviewer = item.get('Teamviewer', '')
    if teamviewer:
        teamviewer = re.search(r'\d{9,10}', teamviewer.replace(' ', ''))
        if teamviewer:
            item['Teamviewer'] = teamviewer.group()

    # Обработка поля AnyDesk
    anydesk = item.get('AnyDesk', '')
    if anydesk:
        anydesk = re.search(r'\d{9,10}', anydesk.replace(' ', ''))
        if anydesk:
            item['AnyDesk'] = anydesk.group()
        

    return item

# Функция для вставки данных в таблицу
def insert_data(conn, table_name, data):
    cursor = conn.cursor()
    for item in data:
        item = validate_workstation_data(item)
        if item is not None:
            owner_title = item.get('owner', {}).get('title') if item.get('owner') else ''
            owner_uuid = item.get('owner', {}).get('UUID') if item.get('owner') else ''
            cursor.execute(f'''
                INSERT OR REPLACE INTO {table_name} (UUID, GK, Teamviewer, AnyDesk, DeviceName, lastModifiedDate, ownerTitle, ownerUUID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.get('UUID'),
                item.get('GK'),
                item.get('Teamviewer'),
                item.get('AnyDesk'),
                item.get('DeviceName'),
                item.get('lastModifiedDate'),
                owner_title,
                owner_uuid
            ))
    conn.commit()

# Основная функция
def main():
    # Получение данных для Workstations
    workstation_data = fetch_data(os.getenv("WORKSTATIONS_METACLASS"), os.getenv("WORKSTATIONS_PARAMS"))
    
    # Подключение к базе данных
    conn = sqlite3.connect('servers.db')
    
    # Создание таблицы Workstations
    create_table(conn, 'Workstations', '''
        UUID TEXT PRIMARY KEY,
        GK TEXT,
        Teamviewer TEXT,
        AnyDesk TEXT,
        DeviceName TEXT,
        lastModifiedDate DATETIME,
        ownerTitle TEXT,
        ownerUUID TEXT               
    ''')
    
    # Вставка данных в таблицу Workstations
    insert_data(conn, 'Workstations', workstation_data)
    
    # Закрытие соединения
    conn.close()

if __name__ == '__main__':
    main()
