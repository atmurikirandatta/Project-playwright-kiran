# Project Playwright Kiran

Automated end-to-end web tests using Playwright (Python), pytest-bdd (Gherkin), Page Object Model, and Allure reporting.

---

## 🚀 Quick Start

python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install --with-deps

---

## 🧪 Run Tests and Generate Allure Report

pytest --alluredir=allure-results

HTML report (requires Allure CLI):
allure generate allure-results -o allure-report --clean
allure open allure-report

## 🏗 CI/CD

- Runs on every push/pull request (see `.github/workflows/`)
- Artifacts and [optional]: Allure HTML is auto-published to GitHub Pages

---

## 📊 View Reports

- **CI artifact:** Download `allure-report` & use:
cd allure-report
python -m http.server

## 🛠 Notes

- Use **headless=True** for CI browser launches.
- Allure CLI **is NOT installed via pip**—see workflow for download.
- The `requirements.txt` is for Python only.
