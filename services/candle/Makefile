run-dev:
	uv run python run.py

build:
	docker build -f Dockerfile -t candles .

run: build
	docker run -it\
		--network redpanda-quickstart-one-broker_redpanda_network\
		-e KAFKA_BOOTSTRAP_SERVERS=redpanda-0:9092\
		candles



