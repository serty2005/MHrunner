import requests
import os, re
from datetime import datetime
from dotenv import load_dotenv
from coreapp.models import Workstation
import django
from django.utils.timezone import make_aware, get_current_timezone

# Загрузка переменных окружения
load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mhrunner.settings')
django.setup()

# Функция для получения данных
def fetch_data():
    url = f'{os.getenv("BASE_URL")}/sd/services/rest/find/{os.getenv("WORKSTATIONS_METACLASS")}?accessKey={os.getenv("ACCESS_KEY")}&attrs={os.getenv("WORKSTATIONS_PARAMS")}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def validate_workstation_data(item):
    # Проверка наличия DeviceName
    if not item.get('DeviceName'):
        return None

    # Преобразование lastModifiedDate в datetime
    last_modified_date = item.get('lastModifiedDate', '')
    if last_modified_date is not None and isinstance(last_modified_date, str):
        try:
            item['lastModifiedDate'] = make_aware(datetime.strptime(last_modified_date, '%Y.%m.%d %H:%M:%S'), timezone=get_current_timezone())
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

def insert_data(data):
    for item in data:
        # Пропускаем данные, если не прошли валидацию
        if not validate_workstation_data(item):
            continue
        try:
            # Пытаемся получить объект Workstation по UUID
            workstation = Workstation.objects.get(UUID=item['UUID'])
        except Workstation.DoesNotExist:
            # Если объекта нет, создаем новый
            workstation = Workstation(UUID=item['UUID'])
        
        # Обновляем поля объекта данными из item
        workstation.GK = item.get('GK')
        workstation.Teamviewer = item.get('Teamviewer')
        workstation.AnyDesk = item.get('AnyDesk')
        workstation.DeviceName = item.get('DeviceName')
        workstation.lastModifiedDate = item.get('lastModifiedDate')
        workstation.ownerTitle = item.get('owner', {}).get('title') if item.get('owner') else ''
        workstation.ownerUUID = item.get('owner', {}).get('UUID') if item.get('owner') else ''
        
        # Сохраняем объект в базе данных
        workstation.save()

# Основная функция
def main():
    # Получение данных для Workstations
    workstation_data = fetch_data()

    # Вставка данных в таблицу Workstations
    insert_data(workstation_data)
    
if __name__ == '__main__':
    main()
