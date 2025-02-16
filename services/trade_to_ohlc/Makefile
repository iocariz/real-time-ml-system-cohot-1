build:
	docker build -t trade-to-ohlc .

run: build
	docker run -it --network=redpanda_network trade-to-ohlc

lint:
	ruff check --fix

format:
	ruff format .

lint-and-format: lint format