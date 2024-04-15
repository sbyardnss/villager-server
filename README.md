# Villager Chess (Server)

An app for assisting chess clubs in coordination and Swiss Tournament management

## Description

Villager Chess is an application for chess clubs to coordinate meetups, play correspondence games, and create/manage Swiss tournaments both in-person and digital. The client side provides an interface and rule set for playing chess with fellow club members using React Chessboard and Chess JS. Anyone can register and create a club of their own or join a previously created club using an optional club password if necessary.


### Dependencies

* Django
* autopep8
* pylint
* djangorestframework
* django-cors-headers
* pylint-django



### Setup
* Enter virtual environment

```sh
pipenv shell
```

* Install dependencies with command below
```sh
pipenv install django autopep8 pylint djangorestframework django-cors-headers pylint-django
```


* Select sqlite database (may vary from mac to windows)
* Mac: Cmd+Shift+P to open preference search
* Select "Sqlite: Open Database"
* Choose "db.sqlite3"



* Migrate Tables

```sh
python3 manage.py migrate
```

* Load fixtures

```sh
python3 manage.py loaddata users tokens players guest_players chess_clubs time_settings community_posts messages tournaments games
```