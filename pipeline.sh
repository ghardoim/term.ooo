#!/bin/bash

echo "STAGE: clean before build"
    rm -r term.exe

echo "STAGE: create environment"
    python -m venv .venv
    source .venv/Scripts/activate

echo "STAGE: install dependencies"
    pip install beautifulsoup4 pyinstaller requests

echo "STAGE: build"
    pyinstaller -w -F findword.py -n "term" --console

echo "STAGE: deploy"
    mv dist/term.exe ./

echo "STAGE: clean after build"
    deactivate
    rm -r build/ dist/ term.spec .venv/