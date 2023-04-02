VERSION = 0.5.0

lint:
	python -m pylint facades_api

format:
	python -m black facades_api

run:
	python -m facades_api

debug:
	python -m facades_api --debug

docker-build:
	docker build --tag kanootoko/facades_api:$(VERSION) .

docker-run:
	docker run --env-file .env --rm --name facades_api

docker-push:
	docker push kanootoko/facades_api:$(VERSION)

docker-update-latest:
	docker tag kanootoko/facades_api:$(VERSION) kanootoko/facades_api:latest
	docker push kanootoko/facades_api:latest

docker-pipeline: docker-build docker-push docker-update-latest

db-revision:
	cd facades_api/db && alembic revision --autogenerate

db-migrate:
	cd facades_api/db && alembic upgrade head