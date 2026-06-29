.PHONY: db-up db-down app-up app-down app-logs mig-create mig-upgrade mig-downgrade mig-recreate web-install web-dev web-build

m ?= new_migration
rev ?= -1

db-up:
	docker compose up -d postgres redis

db-down:
	docker compose stop postgres redis

app-up:
	docker compose up -d --build app

app-down:
	docker compose stop app

app-logs:
	docker compose logs -f app

mig-create:
	docker compose run --rm app alembic revision --autogenerate -m "$(m)"

mig-upgrade:
	docker compose run --rm app alembic upgrade head

mig-downgrade:
	docker compose run --rm app alembic downgrade $(rev)

mig-recreate:
	docker compose run --rm app alembic downgrade base
	docker compose run --rm app alembic upgrade head

web-install:
	npm --prefix frontend install

web-dev:
	npm --prefix frontend run dev

web-build:
	npm --prefix frontend run build
