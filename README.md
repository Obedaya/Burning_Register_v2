# Burning Register v.2.0

Burning Register is a web based cash register to manage inventory, orders and data. The cash register was developed for a cinema but is adaptable to any application.

## Changelog

## Introduction

The frontend of Burning Register is written with Vue or more precisely with Vuetify. This gives the cash register a modern look that is easily customizable. In addition, the cash register is very fast, because through the single page application only one request is sent to the server. The backend is written in Python with FastAPI and uses MongoDB as database. This also makes the backend completely separate from the frontend and can be customized at any time.

## Installation

Clone the repository:
```
git clone https://github.com/Obedaya/Burning_Register_v2.git
```

In the folder create a .env file:
```python
MONGODB_URI=[Your MongoDB URL]
MONGODB_DB_NAME=[Your MongoDB databasename]

UVICORN_PORT=9090

CORS_ORIGINS=["http://localhost:8080","http://[YOUR IP]:8080"]

VUE_APP_DB_ADDRESS='http://[YOUR IP]:9090'
```

## Usage

Run the docker-compose file
```
docker-compose up -d
```