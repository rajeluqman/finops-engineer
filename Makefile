.PHONY: market-build market-check test

market-build:
	python python/market_census/build_market_census.py

market-check:
	python python/market_census/build_market_census.py --validate-only

test:
	python -m unittest tests/test_market_census.py -v
