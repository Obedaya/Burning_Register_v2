# Burning Register v.2.0

Burning Register is a web based cash register to manage inventory, orders and data. The cash register was developed for a cinema but is adaptable to any application.

## Changelog

## Introduction

The frontend of Burning Register is written with Vue or more precisely with Vuetify. This gives the cash register a modern look that is easily customizable. In addition, the cash register is very fast, because through the single page application only one request is sent to the server. The backend is written in Python with FastAPI and uses MongoDB as database. This also makes the backend completely separate from the frontend and can be customized at any time.

## Installation

At the moment there are several steps to run the register:

Clone the repository:
```
git clone https://github.com/Obedaya/Burning_Register_v2.git
```

Go into the backend:
```
cd Burning_Register/services/backend
```

In the folder create a .env file:
```python
MONGODB_URI=[Your MongoDB URL]
MONGODB_DB_NAME=[Your MongoDB databasename]

UVICORN_PORT=9090

CORS_ORIGINS=["http://localhost:8080"]
```

Install backend:
```
pip install ./
```

For the frontend you need to install npm!

## Usage

Go into the backend:
```
cd Burning_Register/services/backend
```

Run the backend:
```
python -m burningbackend
```

---

Go into the frontend:
```
cd Burning_Register/services/frontend
```

Run the frontend:
```
npm run serve
```