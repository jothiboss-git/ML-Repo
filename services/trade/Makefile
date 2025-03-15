run-dev-live:
	copy live.setting.env setting.env
	uv run python run.py

run-dev-historical:
	copy historical.setting.env setting.env
	uv run python run.py



build:
	docker build -f Dockerfile -t trade .

run: build
	docker run -it\
		--network redpanda-quickstart-one-broker_redpanda_network\
		-e KAFKA_BOOTSTRAP_SERVERS=redpanda-0:9092\
		trade



