.PHONY: test test-int lint type up down seed gen-data

test:
	pytest tests/unit -v --cov=app/engine

test-int:
	pytest tests/integration -v

lint:
	ruff check .

type:
	mypy app/

up:
	docker-compose up -d
	
down:
	docker-compose down

gen-data:
	python generator/synth_mep.py --designs 200 --elements-per-design 10 --edge-case-rate 0.15 --out data/designs --eval data/eval --seed 42
