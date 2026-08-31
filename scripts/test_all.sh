#!/usr/bin/env bash
set -euo pipefail

echo "==> Compilation check"
python -m compileall -q generator.py tests

echo "==> Pytest + coverage"
python -m pytest \
  --cov=generator \
  --cov-report=term-missing \
  --cov-report=xml \
  --cov-fail-under=80

echo "==> All checks passed"
