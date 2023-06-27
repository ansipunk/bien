# Run ruff and pytest
default: lint types test-all

# Create virtual environment and install dependencies
bootstrap:
  pdm install -G :all

# Run editor within virtal environment
edit:
  pdm run $EDITOR

# Run static analysis against source code
lint:
	pdm run ruff --fix bien.py test_bien.py

# Check source code type hints
types:
  pdm run mypy bien.py

# Run all project tests
test-all:
  pdm run pytest --cov=. --cov-report=term-missing --cov-report=html

# Run specific tests
test TEST:
	pdm run pytest

# Run all actions with different Python versions
nox:
  pdm run nox

# Build and publish the package
publish:
  pdm publish
