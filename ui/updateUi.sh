#!/bin/bash

# Check if the folder path argument is provided
if [ $# -eq 0 ]; then
  echo "Usage: $0 <folder_path>"
  exit 1
fi

# Get the folder path argument from argv
folder_path=$1

# Check if the specified folder exists
if [ ! -d "$folder_path" ]; then
  echo "Error: The specified folder does not exist."
  exit 1
fi

# Loop through all .ui files in the specified folder
for ui_file in "$folder_path"/*.ui; do
  # Get the base filename without the extension
  base_filename=$(basename "$ui_file" .ui)
  # Convert the .ui file to Python code using pyuic6
  pyuic6 -x "$ui_file" > "$folder_path/${base_filename}.py"
  echo "Converted $ui_file to ${base_filename}.py"
done

echo "Conversion completed for all .ui files in the folder."
