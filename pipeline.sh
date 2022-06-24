#!/bin/bash

if [ ! -d ".venv$1term" ]; then
    echo "STAGE: create environment"
        python -m venv ".venv$1term"
        source ".venv$1term/Scripts/activate"
fi

echo "STAGE: install dependencies"
    python.exe -m pip install --upgrade pip

    if [ "$1" == "find" ]; then
        pip install beautifulsoup4 pyinstaller requests

    elif [ "$1" == "type" ]; then
        pip install playwright
        PLAYWRIGHT_BROWSERS_PATH=0
        python -m playwright install chromium
    fi

echo "STAGE: build deploy finish"
    pyinstaller -c -F "src/$1word.py" -n "$1term" $newarg
    mv "dist/$1term.exe" ./
    deactivate
    rm -r build/ dist/ "$1term.spec"