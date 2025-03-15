## Building better REal time MLsystems

## TODO

 1. Tools
    Code Editor -  cursor

2. Feature Pipeline
  - Ingest the trade from extrernal API
  - Transform the trade into technical indicators
  - Save the technical indicators to a feature store


3. UV - to install the dependencies

   https://github.com/astral-sh/uv  

4. Create trade folder using uv
     go to service foler and excute the command
      uv init trade - it will create the trade folder with the dependencies run.py,project.toml,pyproject.toml
   
   

5. Create a virtual environment
     uv init trade  - it will create the virtual environment and install the dependencies inside trade folder

5. Install Make file
   https://gnuwin32.sourceforge.net/packages/make.htm

  check with LLM  how to install make ?


6. Create a make file in the trade folder which will create vertual environment and install the dependencies
      make run

7. Add loguru to the project for logging- https://github.com/Delgan/loguru
    uv add loguru

8. Add Redpanda to the project for Kafka- https://github.com/redpanda-data/redpanda
   Redpanda is an event streaming platform: it provides the infrastructure for streaming real-time data
     
     docker-compose -f redpanda.yml  up -d

9. Add quixstream to the project for Kafka- https://github.com/quixio/quixstream
   Note : python version is should be 3.9.0
   produce the trade data to the Kafka topic
   Note: install the quixstream before pydantic
    uv add quixstreams

10. Create moke treade service from kraken API for testing
     https://docs.kraken.com/api/docs/websocket-v2/trade/

     - use pydantic and import base model



11. Add pydantic-settings to the project for configuration- https://github.com/pydantic/pydantic-settings
    this is used to manage the configuration in the project
    uv add pydantic-settings 

12 Add websocket to the project for websocket- https://github.com/websocket-client/websocket-client
   uv add websocket-client

13.create a docker file to run the project using uv(used example to create a docker file)
   https://docs.astral.sh/uv/guides/integration/docker/#installing-a-project
    modified makefile to create a docker file



14. Linting and Formatting
     enforce the best practices in the code and catch the potential problems. and formatting to make the code more readable 
     
     uv tool install ruff

     to check error
      ruff check
      to fix issue - ruff check --fix

15. Pre-commit hooks- used to check the code and run ruff check and fix before commit  
      https://pre-commit.com/
      uv tool install pre-commit

      to add pre-commit hooks
      pre-commit install

      -create a pre-commit-config.yaml file in the root of the project
      -add the hooks to the pre-commit-config.yaml file
      to check the pre-commit hooks
      pre-commit run --all-files

16. Create Candle Service
     uv init --no-workspace candle
17. Add loguru,quixstreams,pydantic-settings to the candle service

18. Create technical-indicator service
   uv init --no-workspace technical-inidicator

19. Add loguru,quixstreams,pydantic-settings to the candle service

20> install the TA-LIB library for generate the technical indicator
     https://github.com/TA-Lib/ta-lib-python

     - uv add TA-Lib
     For 64-bit Windows, the easiest way is to get the executable installer:
        Download ta-lib-0.6.4-windows-x86_64.msi.fromabove gitgub
        Run the Installer or run msiexec from the command-line.

       - Prompt for technical indicator
          i want to compute good technical indicator to predict short term crypto prices in python using that 
ta-lib libraty. recommmend 10good indicator for this use case , together with their timeperiod and other hyper paarmeeter and show me the python code to compute them

21. Create a feature store
    uv init --no-workspace feature-store

22. Install hopsworks
     uv add hopsworks
     https://github.com/logicalclocks/hopsworks

22. Create partition at redpanda to achieve parallellism
       that means each bitcoin will be processed by different partition. Example:
       - bitcoin-1 will be processed by partion-1(candleservice 1)(BTC/USD")
       - bitcoin-2 will be processed by partition-2(candleservice 2) ("BTC/EUR")
       - bitcoin-3 will be processed by partition-3 (candleservice 3)("ETH/EUR")
       - bitcoin-4 will be processed by partition-4(candleservice 4)("ETH/USD")
    Command added to docker-compose/Makefile file to add partitions to the trade topic


       https://docs.redpanda.com/current/reference/rpk/rpk-topic/rpk-topic-add-partitions/
       

23. Create NEWS Service
      uv init --no-workspace news

