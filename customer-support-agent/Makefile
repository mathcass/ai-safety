##
# Customer Support Agent Scenario
#
# @file
# @version 0.1

DATE := $(shell date +%Y-%m-%d)

run:
	poetry run streamlit run app.py

simulate-baseline:
	poetry run python chatbot.py baseline-sonnet-and-sonnet-$(DATE)

simulate-comparison:
	poetry run python chatbot.py --guard comparison-sonnet-and-sonnet-$(DATE)

# end
