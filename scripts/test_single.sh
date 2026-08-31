#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: ./scripts/test_single.sh <pytest-test-path>"
  echo "Example: ./scripts/test_single.sh tests/test_generator.py::test_sanitize_identifier"
  exit 1
fi

python -m pytest -v "$1"
