#!/usr/bin/env bash
set -euo pipefail
python -m pytest \
  --cov=generator \
  --cov-report=term-missing \
  --cov-report=xml \
  --cov-fail-under=100