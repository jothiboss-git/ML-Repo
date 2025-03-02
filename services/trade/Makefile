run-dev:
	uv run python run.py

build:
	docker build -f Dockerfile -t trade .

run: build
	docker run -it\
		--network docker-compose_default\
		-e KAFKA_BOOTSTRAP_SERVERS=redpanda:29092\
		trade



