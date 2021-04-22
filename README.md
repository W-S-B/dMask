# dMask
*Снимка*

## Описание:

## Видео, демо и снимки:
Линк към Google Drive -> [Натиснете тук, за да отидете към папката]()

## Какво представлява проекта?
снимково демо

## Как да си изтегля и използвам проекта?
### Изтегляне:
Изтеглете последната версия на проекта (може да видите последната версия отдясно)

### Предварителни настройки:
* Инсталирайте [Python](https://www.python.org/downloads/)
* Инсталирайте [NodeJS](https://nodejs.org/en/download/)

За да можете да ползвате локално проекта, трябва да знаете с каква видео карта разполагате:
#### За NVIDIA:
* Инсталирайте [CUDA11](https://developer.nvidia.com/cuda-11.0-download-archive)
#### За AMD:
* Инсталирайте [ROCm](https://rocmdocs.amd.com/en/latest/)
* ```pip install --user tensorflow-rocm```

### Как да си пуснете проекта?
* Отворете изтегкената папка (след като сте я разархивирали)
* Отворете и терминал (2 пъти)
* ```cd C:\Път\До\Папката``` - в и двата
#### В първи терминал
* ```cd api```
* ```pip install VirtualEnv --user```
* ```pip install VirtualEnvWrapper-win --user```
* ```python -m virtualenv dmask-api```
* ```dmask-api/Scripts/activate```
* ```pip install -r requirements.txt```
* ```$env:FLASK_APP = "api.py"```
#### Във втори терминал
* ```npm ci```
* ```npm start```
#### В първи терминал
* ```npm run start-flask-api```
#### Във втори терминал
* ```npm start```

## Използвани технологии:

#### Web App
* [HTML](https://html.com/)
* [CSS](https://www.w3.org/Style/CSS/Overview.en.html)
* [JavaScript](https://www.javascript.com/)
* [ReactJS](https://reactjs.org/)
* [Flask](https://flask.palletsprojects.com/)
* [SQLite](https://www.sqlite.org/index.html)

#### AI
* [Python](https://www.python.org/)
* [OpenCV](https://opencv.org/)
* [Tensorflow](https://www.tensorflow.org/)

## Информация за авторите на проекта:

* [Алеко Георгиев](https://github.com/AlekoGeorgiev) | Back-end, Local Server
* [Калоян Дойчинов](https://kaloyan.tech) | WebApp - Front-end, API, Run Scripts (Linux)
* [Константин Щерев](https://github.com/KokoShterev) | AI
* [Кристиян Богданов](https://github.com/KristiyanBogdanov) | Back-end
* [Мартин Божилов](https://github.com/TechXTT) | AI
