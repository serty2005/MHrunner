Работает на django
Для запуска требуется:
1. Создать venv с установкой из requirements.txt
2. Добавить .env такого вида:
    BASE_URL = '' /// сюда урл до .com включительно
    ACCESS_KEY = '' /// сюда ключ
    SERVERS_METACLASS = 'objectBase$Server'
    SERVERS_PARAMS = 'UUID,Teamviewer,UniqueID,IP,CabinetLink,owner,title,AnyDesk,DeviceName'

    WORKSTATIONS_METACLASS="objectBase$Workstation"
    WORKSTATIONS_PARAMS="UUID,GK,Teamviewer,AnyDesk,DeviceName,lastModifiedDate,owner"

    COMPANIES_METACLASS="ou$company"
    COMPANIES_PARAMS="UUID,lastModifiedDate,adress,title"
   
4. Сделать python manage.py migrate /// создание скелета базы
   4.1 python manage.py getservers /// заполнение серверами
   4.2 python manage.py getworkstations /// заполнение станциями

5. python manage.py runserver /// по адресу localhost:8000/connections/ будут подключения
