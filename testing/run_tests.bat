ECHO "Running tests"
coverage run -m unittest testing/test.py
ECHO "Generating reports"
coverage html --omit="*/testing*" --directory=testing/htmlcov
ECHO "Opening reports"
start "" "testing/htmlcov/index.html"