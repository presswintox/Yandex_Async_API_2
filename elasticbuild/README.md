# Настройка ElasticSearch

**Ход настройки:**

- докер-компоуз поднимает контейнер эластика с открытым портом 9200 (необходимо для заполнения)
- запускаем в консоли: . elasticbuild/dump.sh

dump.sh:
- Заполняет схемы эластика (используя контейнер python), заполняет Genres, Pesons, Movies. Настройки берутся из .env, логи пишутся в elasticbuild/setupelastic.log

Расположение схем эластика и данных:
- elasticbuild/pyfiles/moviessettings.py
- elasticbuild/movies.json
- elasticbuild/pyfiles/genressettings.py
- elasticbuild/genres.json
- elasticbuild/pyfiles/personssettings.py
- elasticbuild/persons.json


Для соединения с эластиком используется сеть хоста