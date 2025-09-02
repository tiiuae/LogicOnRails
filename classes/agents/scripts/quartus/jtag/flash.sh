#!/bin/bash

# Declaring the variables
first_copy="User_HW.sof"
second_copy="Factory_HW.sof"

curr_dir=$1
file_to_copy=$2
file_path=$curr_dir/$file_to_copy

# Copy the selected file to new files
cp "$file_path" "$curr_dir/$first_copy"
cp "$file_path" "$curr_dir/$second_copy"

echo "Operation completed successfully."


