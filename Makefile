##
# AI Safety
#
# @file
# @version 0.1

run: install
	poetry run python main.py

lab: install
	poetry run jupyter lab

support:
	$(MAKE) -C customer-support-agent

install:
	poetry install

# end
