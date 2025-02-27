#!/bin/bash
# Ensure pip is up to date
pip install --upgrade pip

# Install poetry using pip
pip install poetry

# Ensure poetry is in the system path
export PATH="$HOME/.local/bin:$PATH"

# Install dependencies using poetry
poetry install --no-root

