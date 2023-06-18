# Python Microsevice template/skeleton #

* for use as a base for my python microservices
* it includes a basic endpoint, a Dockerfile, and a pytest test.
* black pylint and isort are used for linting and formatting (can reduce merge confilcts)

Local development:

```pip install -r requirements_local.txt```

```uvicorn main:app --reload```

Docker:

```docker build . -t myimage```

```docker run -p 8000:8000 myimage```

Test:

```pytest -rP```

```curl -X POST -H "Content-Type: application/json" -d '{"string": "test", "integer": 10}' http://localhost:8000/endpoint```