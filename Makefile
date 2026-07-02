.PHONY: up down logs ps migrate smoke demo reset-volumes

up:
	docker compose --profile dev up -d --build

ps:
	docker compose ps

logs:
	docker compose logs -f --tail=100

migrate:
	docker compose --profile dev up migrate

smoke:
	python scripts/smoke_test.py

demo:
	python scripts/run_demo.py

down:
	docker compose --profile dev down

reset-volumes:
	docker compose --profile dev down -v
