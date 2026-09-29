.PHONY: market-build market-check test

market-build:
	python python/market_census/build_market_census.py
	python python/market_census/build_tool_frequency.py

market-check:
	python python/market_census/build_market_census.py --validate-only

test:
	python -m unittest discover -s tests -p 'test_*.py' -v
