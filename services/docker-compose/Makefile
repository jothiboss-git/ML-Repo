#Redpanda Management
start-redpanda:
	docker-compose -f redpanda.yml  up -d

stop-redpanda:
	docker-compose -f redpanda.yml  down

add-partitions:
	docker compose -f redpanda.yml exec redpanda rpk topic add-partitions trade --num 1

#Technical Indicator Pipeline Management -Live
build-technical-indicator-live:
	docker-compose -f technical-indicator-live.yml build

start-technical-indicator-live: build-technical-indicator-live	
	docker-compose -f technical-indicator-live.yml up -d

stop-technical-indicator-live	:
	docker-compose -f technical-indicator-live.yml down

#Technical Indicator Pipeline Management -Historical
build-technical-indicator-historical:
	docker-compose -f technical-indicator-historical.yml build

backfill-technical-indicator-historical: build-technical-indicator-historical	
	$(eval RUN_ID := $(shell powershell -Command "[System.Guid]::NewGuid().ToString()"))
	echo "backfill technical indicator historical run id: $(RUN_ID)"
	set "RUN_ID=$(RUN_ID)" && docker-compose -f technical-indicator-historical.yml up -d

stop-technical-indicator-historical:
	docker-compose -f technical-indicator-historical.yml down

#Clean up the backfill kafka topics
clean-backfill-kafka-topics:
	@echo "Cleaning up the backfill kafka topics which contains historical data"
	docker compose -f redpanda.yml exec redpanda rpk topic delete --topic -r ".*historical*"
	



