#!/bin/bash

# Check for different arguments
if [ "$1" == "--dev" ]; then
    python -m uvicorn main:app --reload 
elif [ "$1" == "--prod" ]; then
    python -m uvicorn main:app 
else
    echo "Usage: ./run.sh [option]"
    echo "Options:"
    echo "  --dev: App will listen for changes and restart when you modify it."
    echo "  --prod: Run in production mode"
fi
