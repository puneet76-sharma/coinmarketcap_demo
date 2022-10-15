# coinmarketcap_demo

# Instructions:

git clone https://github.com/puneet76-sharma/coinmarketcap_demo.git

cd coinmarketcap_demo

Create Env
python m -venv venv

To activate Env 
venv\Scripts\activate >>> for win users
source venv/bin/activate >> for linux

pip install -r requirements.txt

create DB name "coinmarket" in postgresql

python manage.py migrate

python manage.py runserver


APIS :- 
1) http://127.0.0.1:8000/create-coins/  - Post request
2) http://127.0.0.1:8000/get-coins/    - Get request
