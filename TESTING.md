TEST COMMANDS

Install:
    python -m pip install -r requirements-dev.txt

Basic:
    ./scripts/test.sh

Verbose:
    ./scripts/test_verbose.sh

Quiet/fast output:
    ./scripts/test_fast.sh

Coverage:
    ./scripts/test_coverage.sh

Coverage + HTML:
    ./scripts/test_coverage_html.sh
    open htmlcov/index.html

Enforce 80% coverage:
    ./scripts/test_coverage_enforce.sh

Compile generator/tests:
    ./scripts/test_compile.sh

Run one test:
    ./scripts/test_single.sh tests/test_generator.py::test_sanitize_identifier

Run full local CI-style suite:
    ./scripts/test_all.sh

Direct pytest equivalents:
    python -m pytest
    python -m pytest -v
    python -m pytest -q
    python -m pytest --cov=generator --cov-report=term-missing
    python -m pytest --cov=generator --cov-report=html
    python -m pytest --cov=generator --cov-report=term-missing --cov-report=xml --cov-fail-under=80
