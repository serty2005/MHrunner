import os, re
import django
from dotenv import load_dotenv
import requests
from coreapp.models import Server


# Загрузка переменных окружения
load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mhrunner.settings')
django.setup()

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
            cabinet_link = re.sub(r'https://partners\.iiko\.ru/(ru|en)/cabinet/clients\.html\?mode=showOne&id=', 'https://partners.iiko.ru/v2/ru/cabinet/client-area/index.html?clientId=', cabinet_link)
        item['CabinetLink'] = cabinet_link
    
    ip = item.get('IP', '')
    if ip and '.iiko.it' in ip:
        match = re.search(r'https://(.*?\.iiko\.it)', ip)
        if match:
            item['cleared_ip'] = match.group(1)

    return item

def insert_data(data):
    for item in data:
        # Пропускаем данные, если не прошли валидацию
        if not validate_data(item):
            continue
        try:
            # Пытаемся получить объект Server по UUID
            server = Server.objects.get(UUID=item['UUID'])
        except Server.DoesNotExist:
            # Если объекта нет, создаем новый
            server = Server(UUID=item['UUID'])
        owner_uuid = item.get('owner', {}).get('UUID') if item.get('owner') else ''
        owner_title = item.get('owner', {}).get('title') if item.get('owner') else ''

        # Обновляем поля объекта данными из item
        server.Teamviewer = item.get('Teamviewer', None)
        server.UniqueID = item.get('UniqueID', None)
        server.IP = item.get('IP', None)
        server.CabinetLink = item.get('CabinetLink', None)
        server.title = item.get('title', None)
        server.AnyDesk = item.get('AnyDesk', None)
        server.DeviceName = item.get('DeviceName', None)
        server.ownerUUID = owner_uuid
        server.ownerTitle = owner_title
        server.cleared_ip = item.get('cleared_ip', None)
        
        # Сохраняем объект в базу данных
        server.save()

# Основная функция
def main():
    data = fetch_data()
    insert_data(data)

if __name__ == '__main__':
    main()
