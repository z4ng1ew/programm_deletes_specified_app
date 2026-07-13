# how_to_delete_sublaime_text













s@Vivo:~$ wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo gpg --dearmor -o /usr/share/keyrings/sublimehq-archive.key
[sudo] пароль для s: 
s@Vivo:~$ echo "deb [signed-by=/usr/share/keyrings/sublimehq-archive.key] https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
deb [signed-by=/usr/share/keyrings/sublimehq-archive.key] https://download.sublimetext.com/ apt/stable/
s@Vivo:~$ sudo apt update
Сущ:1 http://ru.archive.ubuntu.com/ubuntu noble InRelease
Сущ:2 http://ru.archive.ubuntu.com/ubuntu noble-updates InRelease                         
Сущ:3 http://ru.archive.ubuntu.com/ubuntu noble-backports InRelease                       
Сущ:4 https://dl.google.com/linux/chrome-stable/deb stable InRelease                      
Сущ:5 https://download.docker.com/linux/ubuntu noble InRelease                            
Сущ:6 http://security.ubuntu.com/ubuntu noble-security InRelease                          
Пол:7 https://pkgs.tailscale.com/stable/ubuntu noble InRelease                            
Пол:8 https://repo.librewolf.net librewolf InRelease [5 665 B]                            
Пол:9 https://download.sublimetext.com apt/stable/ InRelease [3 320 B]                    
Сущ:10 https://ppa.launchpadcontent.net/mozillateam/ppa/ubuntu noble InRelease            
Сущ:11 https://ppa.launchpadcontent.net/xtradeb/apps/ubuntu noble InRelease       
Пол:12 https://download.sublimetext.com apt/stable/ Packages [11,9 kB]            
Получено 27,4 kB за 3с (10,4 kB/s)         
Чтение списков пакетов… Готово
Построение дерева зависимостей… Готово
Чтение информации о состоянии… Готово         
Может быть обновлено 92 пакета. Запустите «apt list --upgradable» для их показа.
s@Vivo:~$ sudo apt install sublime-text
Чтение списков пакетов… Готово
Построение дерева зависимостей… Готово
Чтение информации о состоянии… Готово         
Следующие НОВЫЕ пакеты будут установлены:
  sublime-text
Обновлено 0 пакетов, установлено 1 новых пакетов, для удаления отмечено 0 пакетов, и 92 пакетов не обновлено.
Необходимо скачать 15,9 MB архивов.
После данной операции объём занятого дискового пространства возрастёт на 54,3 MB.
Пол:1 https://download.sublimetext.com apt/stable/ sublime-text 4200 [15,9 MB]
Получено 15,9 MB за 2мин 31с (106 kB/s)                                                   
Выбор ранее не выбранного пакета sublime-text.
(Чтение базы данных … на данный момент установлено 291350 файлов и каталогов.)
Подготовка к распаковке …/sublime-text_4200_amd64.deb …
Распаковывается sublime-text (4200) …
Настраивается пакет sublime-text (4200) …
Обрабатываются триггеры для desktop-file-utils (0.27-2build1) …
Обрабатываются триггеры для hicolor-icon-theme (0.17-2) …
Обрабатываются триггеры для gnome-menus (3.36.0-1.1ubuntu3) …
s@Vivo:~$ free -h
               всего        занят        своб      общая  буф/врем.   доступно
Память:         15Gi       5,2Gi       4,0Gi       159Mi       5,5Gi       9,8Gi
Подкачка:      4,0Gi          0B       4,0Gi
s@Vivo:~$ 

















- распиши гайд по удалению, так что бы уудалить полностью и освободить память, а также помоги сделать полную очистку памяти


