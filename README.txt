Files to add to your repository:

generator_fixed.py
tests/test_generator.py
requirements-dev.txt
pytest.ini
.github/workflows/test.yml

Local commands:

    python -m pip install -r requirements-dev.txt

    python -m pytest

Coverage:

    python -m pytest --cov=generator_fixed --cov-report=term-missing

HTML coverage:

    python -m pytest --cov=generator --cov-report=html

Then open:

    htmlcov/index.html
