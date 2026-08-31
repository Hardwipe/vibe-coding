#!/usr/bin/env bash
set -euo pipefail
python -m pytest --cov=generator --cov-report=term-missing --cov-report=html
echo "HTML coverage report generated at htmlcov/index.html"
