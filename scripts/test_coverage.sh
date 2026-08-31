#!/usr/bin/env bash
set -euo pipefail
python -m pytest --cov=generator --cov-report=term-missing
