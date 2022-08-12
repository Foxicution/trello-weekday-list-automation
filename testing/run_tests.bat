ECHO "Running tests"
coverage run -m unittest testing/test.py
ECHO "Generating reports"
coverage html --omit="*/testing*"
ECHO "Opening reports"
start "" "htmlcov/index.html"