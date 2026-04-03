
all:up

build : 
	docker compose build

up : build
	docker compose up

down :
	docker compose down

test-unit :
	uv run pytest tests/test_task.py tests/test_api.py 

test-integration : 
	docker compose up -d 
	sleep 5
	uv run pytest tests/integration/test_integration.py

