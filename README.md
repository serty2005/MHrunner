Работает на django
Для запуска требуется:
1. Создать venv с установкой из requirements.txt
2. Добавить .env такого вида:  
>BASE_URL = '' # сюда урл до .com включительно  
>ACCESS_KEY = '' # сюда ключ  
>SERVERS_METACLASS = 'objectBase$Server'  
>SERVERS_PARAMS = 'UUID,Teamviewer,UniqueID,IP,CabinetLink,owner,title,AnyDesk,DeviceName'  
>WORKSTATIONS_METACLASS="objectBase$Workstation"  
>WORKSTATIONS_PARAMS="UUID,GK,Teamviewer,AnyDesk,DeviceName,lastModifiedDate,owner"  
>COMPANIES_METACLASS="ou$company"  
>COMPANIES_PARAMS="UUID,lastModifiedDate,adress,title"  
   
4. Выполнить из под venv  
   4.0 <code>python ./mhrunner/manage.py migrate</code> # создание скелета базы  
   4.1 <code>python ./mhrunner/manage.py getservers</code> # заполнение серверами  
   4.2 <code>python ./mhrunner/manage.py getworkstations</code> # заполнение станциями  
   4.3 <code>python ./mhrunner/manage.py createsuperuser</code> # добавляем админа для админки

5. <code>python manage.py runserver</code> # по адресу localhost:8000/connections/ будут подключения  
6. В админке localhost:8000/admin/ доступно редактирование и обновление объектов  