env:
  ifneq ("$(wildcard .env)","")
    include .env
    export $(shell sed 's/=.*//' .env)
  endif

runserver-dev: env
	python3 main.py
