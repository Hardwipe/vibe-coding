# Vibe Coding: Python Project Generator

A practical demonstration of **vibe coding** a functional Python application and progressively adding traditional software engineering practices around the generated implementation.

This project contains an interactive CLI-driven **synthetic Python project generator** capable of creating configurable Python source files containing functions, classes, methods, imports, type hints, docstrings, and randomized logic.

The project is then validated using **pytest**, **pytest-cov**, Python compilation checks, shell-based testing utilities, and a **GitHub Actions CI pipeline** with 100% statement coverage enforcement.

## What Is Vibe Coding?

For the purposes of this project, vibe coding follows an iterative AI-assisted development workflow:

```text
Idea / Requirements
        ↓
AI-Generated Implementation
        ↓
Execute the Software
        ↓
Observe the Result
        ↓
Identify Problems
        ↓
Modify the Implementation
        ↓
Automated Testing
        ↓
Continuous Integration
        ↓
Repeat
```

Rather than manually implementing every individual piece of source code, the developer focuses on describing the desired behavior, evaluating the generated implementation, and progressively building confidence in its correctness.

The important part is verification.

Generated code should not automatically be assumed to work simply because it was successfully generated or because the application executed without immediately crashing.

This project demonstrates that distinction by taking vibe-coded software and surrounding it with increasingly rigorous automated verification.

---

# Python Project Generator

`generator.py` provides an interactive CLI for generating synthetic Python projects.

Run it with:

```bash
python generator.py
```

The generator asks how the generated project should be configured.

Example:

```text
============================================================
PYTHON SYNTHETIC PROJECT GENERATOR
============================================================

Press Enter to accept any default.

Project name [generated_project]:
Output directory [./output]:
Number of Python files [3]:
Functions per file [3]:
Classes per file [2]:
Methods per class [3]:

Generated file prefix [module]:
Function name prefix [generated_function]:
Class name prefix [GeneratedClass]:
Method name prefix [generated_method]:

Include imports? [Y/n]:
Include docstrings? [Y/n]:
Include type hints? [Y/n]:
Create __init__.py? [Y/n]:
Create main.py? [Y/n]:

Randomize generated function logic? [Y/n]:
Random seed [leave blank for random]:
```

Pressing **Enter** accepts the displayed default, allowing a complete project to be generated without manually configuring every option.

---

## Generator Features

The generator currently supports:

* Multiple Python files
* Configurable functions per file
* Configurable classes per file
* Configurable methods per class
* Custom project names
* Custom output directories
* Custom module naming prefixes
* Custom function naming prefixes
* Custom class naming prefixes
* Custom method naming prefixes
* Python type hints
* Generated docstrings
* Default imports
* Custom imports
* Optional `__init__.py`
* Optional `main.py`
* Randomized function logic
* Randomized method logic
* Deterministic generation using random seeds
* Python identifier sanitization
* Filename sanitization
* CLI input validation
* Generation summaries

---

# Example Generated Project

A generated project may look like:

```text
output/
└── generated_project/
    ├── __init__.py
    ├── main.py
    ├── module_1.py
    ├── module_2.py
    └── module_3.py
```

A generated module may contain code similar to:

```python
from pathlib import Path
from typing import Any


def generated_function_1_1(values: list[float]) -> object:
    """Automatically generated function: generated_function_1_1."""
    if not values:
        return None
    return max(values)


class GeneratedClass1_1:
    """Automatically generated class: GeneratedClass1_1."""

    def __init__(self, values: list[float]) -> None:
        self.values = values

    def generated_method_1_1(self) -> object:
        """Automatically generated method: generated_method_1_1."""
        return sum(self.values)

    def generated_method_1_2(self) -> object:
        """Automatically generated method: generated_method_1_2."""
        return sorted(self.values)
```

The generated source code itself acts as a **synthetic software dataset** that can be used for automated testing, static analysis, compilation testing, performance testing, CI experimentation, and other development tooling.

---

# Deterministic Generation

Randomized generation can make automated testing difficult because the output changes between executions.

The generator therefore supports a random seed.

For example:

```text
Random seed [leave blank for random]: 100
```

Using the same configuration and random seed produces the same randomized sequence.

This makes it possible to perform reproducible testing against generated projects.

Conceptually:

```text
Configuration + Seed
        ↓
Generator
        ↓
Predictable Output
        ↓
Regression Testing
```

Leave the random seed blank when deterministic output is not required.

---

# Testing

The project uses **pytest** for automated testing.

Install the development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the complete test suite:

```bash
python -m pytest
```

Or use the included testing scripts:

```bash
./scripts/test.sh
```

---

## Test Coverage

Coverage is measured using `pytest-cov`.

Run tests with terminal coverage reporting:

```bash
./scripts/test_coverage.sh
```

Equivalent command:

```bash
python -m pytest \
  --cov=generator \
  --cov-report=term-missing
```

Example output:

```text
Name           Stmts   Miss  Cover
----------------------------------
generator.py     223      0   100%
----------------------------------
TOTAL            223      0   100%
```

The current test suite achieves:

**100% statement coverage of `generator.py`.**

Coverage does not prove that software is completely correct.

Instead, it tells us that every executable statement measured by the coverage tool was executed during the test suite.

The quality and completeness of the assertions remain important.

---

# HTML Coverage Report

Generate an interactive HTML coverage report with:

```bash
./scripts/test_coverage_html.sh
```

Or:

```bash
python -m pytest \
  --cov=generator \
  --cov-report=html
```

The report is generated under:

```text
htmlcov/
```

On macOS, open it with:

```bash
open htmlcov/index.html
```

The HTML report provides a line-by-line visualization of which portions of the source code were executed during testing.

---

# Coverage Enforcement

The project can enforce the required coverage percentage automatically.

Run:

```bash
./scripts/test_coverage_enforce.sh
```

The underlying command uses:

```bash
python -m pytest \
  --cov=generator \
  --cov-report=term-missing \
  --cov-report=xml \
  --cov-fail-under=100
```

The command fails if coverage drops below **100%**.

This means adding new source code without corresponding test coverage can cause both local verification and CI verification to fail.

---

# Testing Scripts

Several shell scripts are included for common development workflows.

### Standard Tests

```bash
./scripts/test.sh
```

Runs the normal pytest suite.

### Verbose Tests

```bash
./scripts/test_verbose.sh
```

Displays additional information for each executed test.

### Minimal Output

```bash
./scripts/test_fast.sh
```

Runs pytest with reduced terminal output.

### Terminal Coverage

```bash
./scripts/test_coverage.sh
```

Runs tests and displays coverage directly in the terminal.

### HTML Coverage

```bash
./scripts/test_coverage_html.sh
```

Generates the HTML coverage dashboard.

### Coverage Enforcement

```bash
./scripts/test_coverage_enforce.sh
```

Requires 100% statement coverage.

### Python Compilation Check

```bash
./scripts/test_compile.sh
```

Checks that the generator and test source files compile successfully.

### Individual Test

A specific pytest test can be executed with:

```bash
./scripts/test_single.sh tests/test_generator.py::test_sanitize_identifier
```

### Complete Local CI Check

Before pushing changes, run:

```bash
./scripts/test_all.sh
```

This performs the broader local verification process, including compilation checks, automated tests, and coverage enforcement.

---

# Why Compilation Testing Matters

One of the first issues discovered during development was malformed indentation inside generated Python functions.

The generator itself executed successfully and created the requested files.

However, some of those files contained code similar to:

```python
if not values:
        return None
    return max(values)
```

The generator had therefore technically completed its immediate task of creating files while still producing invalid output.

The corrected output was:

```python
if not values:
    return None
return max(values)
```

This demonstrates an important distinction:

> Successful execution of the generator does not guarantee correctness of the generated output.

The automated test suite now compiles generated Python files so syntax and indentation problems can be detected automatically.

This turns a manually discovered bug into a permanent regression test.

---

# GitHub Actions

Continuous integration is provided through GitHub Actions.

The workflow executes when:

* A pull request targets `main`
* Code is pushed to `main`

The CI matrix currently tests:

```text
Python 3.11
Python 3.12
Python 3.13
```

Each environment:

1. Checks out the repository
2. Installs the configured Python version
3. Upgrades `pip`
4. Installs development dependencies
5. Executes pytest
6. Measures code coverage
7. Displays coverage in the Actions logs
8. Enforces 100% statement coverage
9. Generates HTML coverage
10. Generates XML coverage
11. Uploads coverage reports as GitHub Actions artifacts

---

# GitHub Actions Coverage

The CI test command generates three forms of coverage output:

```bash
python -m pytest \
  --cov=generator \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-report=xml \
  --cov-fail-under=100
```

### Terminal Report

`term-missing` displays coverage directly inside the GitHub Actions logs.

### HTML Report

`html` generates a browsable line-by-line coverage dashboard.

### XML Report

`xml` generates:

```text
coverage.xml
```

which can also be consumed by external coverage and code-quality tooling.

---

# GitHub Actions Artifacts

Each Python version uploads its own coverage reports.

Artifacts are named using the corresponding Python version:

```text
coverage-html-python-3.11
coverage-html-python-3.12
coverage-html-python-3.13

coverage-xml-python-3.11
coverage-xml-python-3.12
coverage-xml-python-3.13
```

Coverage artifacts are retained for **14 days**.

After a workflow finishes:

```text
GitHub Repository
        ↓
Actions
        ↓
Python Tests
        ↓
Workflow Run
        ↓
Artifacts
```

Download the desired HTML coverage artifact, extract it, and open:

```text
index.html
```

to inspect the complete coverage report locally.

---

# Project Structure

The repository is structured approximately as:

```text
vibe-coding/
│
├── generator.py
├── requirements-dev.txt
├── pytest.ini
├── README.md
├── .gitignore
│
├── tests/
│   └── test_generator.py
│
├── scripts/
│   ├── test.sh
│   ├── test_all.sh
│   ├── test_compile.sh
│   ├── test_coverage.sh
│   ├── test_coverage_enforce.sh
│   ├── test_coverage_html.sh
│   ├── test_fast.sh
│   ├── test_single.sh
│   └── test_verbose.sh
│
└── .github/
    └── workflows/
        └── test.yml
```

Generated projects are written separately under the configured output directory.

---

# Local Development Setup

Clone the repository:

```bash
git clone <repository-url>
cd vibe-coding
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the generator:

```bash
python generator.py
```

Run the tests:

```bash
./scripts/test.sh
```

Run the complete local verification:

```bash
./scripts/test_all.sh
```

---

# Development Workflow

A typical development cycle for this repository is:

```text
Create / modify functionality
        ↓
Run generator
        ↓
Inspect generated output
        ↓
Run pytest
        ↓
Run coverage
        ↓
Run full local checks
        ↓
Commit changes
        ↓
Push development branch
        ↓
Open pull request
        ↓
GitHub Actions executes
        ↓
Tests + 100% coverage required
        ↓
Inspect downloadable coverage reports
        ↓
Merge
```

This creates multiple layers of verification between AI-generated implementation and production code.

---

# The Goal

The purpose of this repository is not simply to generate random Python files.

It is an experiment in combining **AI-assisted development with traditional software engineering verification**.

The basic philosophy is:

```text
Vibe Code
    ↓
Execute
    ↓
Observe
    ↓
Test
    ↓
Measure
    ↓
Automate
    ↓
Verify
    ↓
Iterate
```

AI can dramatically accelerate implementation, but implementation speed does not remove the need for verification.

This project explores how quickly functional software can be developed with AI while still introducing automated testing, reproducibility, regression protection, coverage measurement, and continuous integration around that software.

In other words:

**Vibe code the implementation, then engineer confidence into the result.**
