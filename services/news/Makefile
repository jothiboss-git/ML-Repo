run-dev:
	uv run python run.py

build:
	docker build -f Dockerfile -t news-service .

run: build
	docker run -it\
		--network redpanda-quickstart-one-broker_redpanda_network\
		-e KAFKA_BOOTSTRAP_SERVERS=redpanda-0:9092\
		news-service

#build:
#	docker build -f Dockerfile -t technical-indicator .

#run: build
#	docker run -it\
#		--network redpanda-quickstart-one-broker_redpanda_network\
#		-e KAFKA_BOOTSTRAP_SERVERS=redpanda-0:9092\
#		technical-indicator



