#!/bin/bash

# Kill any running Python server
lsof -ti:8000 | xargs kill

# Generate the static site
python3 generate_site.py

# Change to the docs directory
cd docs

# Start the Python server
python3 -m http.server &

# Open the default web browser
python3 -c "import webbrowser; webbrowser.open('http://localhost:8000')"

# Go back to the parent directory
cd ..