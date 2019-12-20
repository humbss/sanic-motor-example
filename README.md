# sanic-motor-example
Python 3+ event-loop application using Sanic as microframework and Motor in the persistence layer.

![sanic](https://raw.githubusercontent.com/huge-success/sanic-assets/master/png/sanic-framework-logo-white-400x97.png)

## Setup Project

1. Create virtual environment (in clone directory):

    `python3 -m venv ./envi`

    Activate the new environment

    `source ./envi/bin/activate`

2. Install dependencies

    `pip3 install -r requirements.txt `

3. Create .env file with the following content:

    `SANIC_dbhost=localhost`

    `SANIC_dbport=27017`

4. Bring mongp up with docker-compose file:

    `docker-compose up`

5. Run app

    `make runserver-dev`

```bash
.
├── api
│   ├── __init__.py
│   ├── routes.py
│   ├── user_API.py ---> (REST API Layer)
│   └── user_service.py ---> (Business Layer)
├── db
│   ├── __init__.py
│   └──  motor_connection.py ---> (DB Connection handler)
├── tests
│   └──  test_user.py ---> (User API unit tests)
├── docker-compose.yml ---> (Docker compose with Mongo DB service)
├── main.py ---> (APP ENTRYPOINT)
├── Makefile
├── README.md
└── requirements.txt ---> (Required libs file)

```

## Test Requests

`[POST]` localhost:8000/user/

Payload:

    {
        "first":"55555555",
        "last":"1212"
    }
    

`[GET]` localhost:8000/user/INSERTED-ID

## Unit Tests

The directory `tests` has the unit tests (PyTest) files, you can invoke the test execution with the command:

`pytest`
 
## DOC

Swagger URL: `http://localhost:8000/swagger/`
