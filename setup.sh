#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@example.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]\n\
primaryColor = \"#3b82f6\"\n\
backgroundColor = \"#ffffff\"\n\
secondaryBackgroundColor = \"#f3f4f6\"\n\
textColor = \"#1f2937\"\n\
" > ~/.streamlit/config.toml

# Download spaCy model
python -m spacy download en_core_web_sm