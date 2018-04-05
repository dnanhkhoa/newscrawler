#!/bin/bash
find .. -iname "__pycache__" -type d -exec rm -r "{}" \;
