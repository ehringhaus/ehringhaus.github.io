#!/bin/bash

# Blog directory
cd /Users/justin/Desktop/blog

# Kill any running Python server
lsof -ti:8000 | xargs kill

# Generate the static site
python3 generate_site.py

# Change to the docs directory
cd docs

# Start the Python server in the background
python3 -m http.server 8000 &

# Store the server process ID
server_pid=$!

# Open the default web browser
python3 -c "import webbrowser; webbrowser.open('http://localhost:8000')"

# Wait for the server process to finish
wait $server_pid