VERSION = 0.2.0

lint:
	pylint facades_api --max-line-length 120

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
