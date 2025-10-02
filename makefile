.PHONY: test
test:
	pytest --alluredir=allure-results
	allure generate allure-results -o allure-report --clean

.PHONY: open-report
open-report:
	allure open allure-report
