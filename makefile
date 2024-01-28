test:
	docker compose -f docker-compose-test.yaml down
	docker compose -f docker-compose-test.yaml run --rm django-api-test || true
	docker compose -f docker-compose-test.yaml down
