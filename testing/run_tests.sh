#!/bin/bash
echo "Running tests..."
coverage run -m unittest testing/test.py
echo "Generating coverage report..."
coverage html --omit="*/testing*" --directory=testing/htmlcov
echo "Opening coverage report..."
firefox testing/htmlcov/index.html