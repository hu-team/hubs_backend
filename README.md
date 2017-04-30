# Hubs Backend

## Installation

1. Create virtualenv ```virtualenv -p python3 env```. (https://virtualenv.pypa.io/en/stable/userguide/#usage)
2. Activate virtualenv. ```source env/bin/activate``` or ```env\Scripts\Activate.bat```.
3. Install dependencies. ```pip install -r requirements.txt -U```
4. Go to src/config/settings and duplicate local.default.py to local.py and change contents.
5. Execute migrations. (in src folder: ```./manage.py migrate```).
5. Create cache table. (in src folder: ```./manage.py createcachetable```).
5. (Optional) Generate sample_data. (in src folder: ```./manage.py sample_data```).

## Starting

1. Make sure your virtualenv is active. ```source env/bin/activate``` or ```env\Scripts\Activate.bat```.
2. Make sure you migrate all pending migrations (after pull). From src folder: ```./manage.py migrate```.
3. Start development server. From src folder: ```./manage.py runserver_plus 127.0.0.1:8000```.
4. Login with admin account (if sample data: admin/Welkom01).
