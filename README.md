## General Structure
```
├── ...                           # .env file and /env folder
├── .python-version               # defines a python version to be run by `pyenv` and with `pipenv`
├── src                    
│   ├── models                    # defines data models for both api and db 
│   │   └── ...              
│   ├── resources                 # contains all api endpoints and queries specific to the request for a resource
│   │   └── ...              
│   ├── server                    # Exports `server.instance` server class with Flask `app` and `db` objects
│   │   └── instance.py              
│   ├── config.py                 # Flask server Config object, injected in `server/instance.py`
│   ├── main.py                   # imports api resources and runs server
│   └── ...                       # misc server scripts (create_db, seed_db, etc.)
├── conftest.py                   # creates app fixture and runs all tests with the `pytest` cmd
└── tests 
    ├── resources                 # this corresponds to src/resources
    │   └── test_****.py          # all tests must be prefixed with `test_`
    └── ...
```

## With Docker (recommended)
###  to start
```
docker-compose up --build
```

### to take down
```
docker-compose down -v
```

### to init db
```
# build db
docker-compose exec api python src/create_db.py

# connect to db
docker-compose exec db psql --username=metrics_user --dbname=metrics_db

# seed db
docker-compose exec api python src/seed_db.py

# inspect db 
docker volume inspect metrics-selfservice_postgres_data
```

## With pyenv
### installations
```
brew install pyenv
brew install pipenv
```

There is a chance with certain MacOS versions you will need to run the following before proceeding: see [this github issue](https://github.com/pyenv/pyenv/issues/1107)

```
sudo mv /usr/local/include /usr/local/include_old
sudo mkdir /usr/local/include
sudo chown -R $(whoami) /usr/local/include
```

```
# Install the desired python version
pyenv install
# configure pipenv
pip install --user pipenv
```
(Some text editors my display errors if not pointed to proper python version, but virtual env should bypass this)

App can then be run within the pipenv shell
```
# Initialises environment variables 
# and loads dependencies
pipenv shell
$ pipenv run python src/main.py
```
or run in background
```
pipenv run python src/main.py
```
within the pipenv shell, you can execute scripts.  scripts can also be run through pipenv command line.
```
pipenv run python src/create_db.py
pipenv run python src/seed_db.py
```