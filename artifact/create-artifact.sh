#!/bin/bash

CWD="$(pwd)"
ARTIFACT_FILENAME="shippostbot-$(git describe --always --long --dirty).zip"
ARTIFACT_PATH="$(realpath $(dirname $0))/$ARTIFACT_FILENAME"

cd "$(git rev-parse --show-toplevel)"
echo $ARTIFACT_PATH
zip -9 "$ARTIFACT_PATH" $(git ls-files)
cd .venv/lib/python3.7/site-packages
zip -gr9 "$ARTIFACT_PATH" .
cd "$CWD"
