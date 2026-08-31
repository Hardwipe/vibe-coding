#!/usr/bin/env bash
set -euo pipefail
python -m compileall -q generator.py tests
echo "Python compilation checks passed."
