# greenway api

### NB:
  toutes ces commandes se font à la racine du projet

#### 1 - start db container :
- make dev

#### 2 - create env

- python3 -m venv env
- source env/bin/activate

#### 2 - start dev server :

- pip install -r requirements.txt
- uvicorn app.main:app --host localhost --port 8000 --reload

#### techonologies :

- orm : pymongo
- framework : fastapi
- docker