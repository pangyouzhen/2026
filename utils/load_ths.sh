#!/bin/bash

# Get yesterday's date in YYYY-MM-DD format
yesterday=$(date -d "yesterday" +%Y-%m-%d)

# Construct the input file path
input_file="../sentiment/strong/strong_${yesterday}.csv"

# Run the first Python script
python get_strong_code.py --input "$input_file"

# Check if the first script created code.txt
if [ -f "code.txt" ]; then
  # Run the second Python script
  python txt2sel2.py code.txt code2.sel
else
  echo "Error: code.txt not found. The first script may have failed."
fi

mv code2.sel ~/Desktop/code2.sel