# mixxit__get_user_consumption

This application is used to obtain the data consumption of Mixxit users.

## Virtual environment

### creating a virtual environment (Windows)

python3 -m venv .venv_windows

### activate virtual environment

./.venv_windows/Scripts/Activate.ps1

## How to install the application

`python3 -m pip install -r requirements.txt`
or
`python -m pip install -r requirements.txt`

## database configuration

The database configuration elements can be found in the **_database.ini** file.

Below is the content of the _database.ini file (replace the value to the right of the "=" with the real values):

```txt

[postgresql]
host=the_host
database=name_of_the_database
user=name_of_the_user
```

## database password

### In case of production

The **root** is the parent of the getUserConsumption folder

* In the root of the project, create a file named **.env_prod**
* The content is as follows:

```txt
# prod environment

# database password

db_password = password without quotes nor space
```

### In case of development

The **root** is the parent of the getUserConsumption folder

* In the root of the project, create a file named **.env_dev**
* The content is as follows:

```txt
# dev environment

# database password

db_password = password without quotes nor space
```

## Launch the application

To execute the application, type the command in the terminal from the root of the project
(The root of the project is the parent of the **getUserConsumption** folder):

### View all events on a given period

```python
python3 getUserConsumption get_all_activities_between_dates from:2021-01-01 to:2021-01-02 prod

```

### View the usage of a user on a given period (via iccid)

```python
python3 getUserConsumption get_user_consumption iccid:89852351019350034494 from:2021-01-01 to:2021-02-01 prod

```
