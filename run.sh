#!/bin/bash

unbuffer python3 src/main.py |& grep --line-buffered -v "Corrupt JPEG data:"