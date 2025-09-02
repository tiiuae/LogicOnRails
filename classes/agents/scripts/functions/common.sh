RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
LIGHT_BLUE="\e[94m"
ENDCOLOR="\e[0m"


#############################################################################
# Function to read from a file and append paths to the file_paths array
declare -a file_paths=()
function read_file {
  while IFS= read -r line || [[ -n "$line" ]]; do
    # Check if the line starts with #. If not, add it to the list
    if [[ $line != \#* ]]; then
      file_paths+=("$line")
    fi
  done < "$1"
}

#############################################################################
declare -a ips_paths=()
function break_data {
  remove_str=$1
  extra_data=$2
  for eachEntry in "${@:3}"; do
    if echo "$eachEntry" | grep -q "$remove_str"; then
      thisEntry=${eachEntry//$remove_str/}
      thisEntry="${thisEntry%.ip}$extra_data"
      ips_paths+=("$thisEntry")
    fi
  done 
}

#############################################################################
function remove_comments() {
  input_file="$1"
  output_file="$2"
  if [[ ! -f "$input_file" ]]; then
    echo "Input file does not exist."
    return 1
  fi
  : > "$output_file"
  while IFS= read -r line; do
    if [[ ! "$line" =~ ^# ]]; then
      echo "$line" >> "$output_file"
    fi
  done < "$input_file"
}

#############################################################################
remove_files() {
    for file in *; do
        if [[ -f "$file" && "$file" == *$1 && "$file" != *$2* ]]; then
            rm "$file"
        fi
    done
}

#############################################################################
export_variable() {
  local name="$1"
  local value="$2"
  declare -gx "$name=$value "
  echo exporting "$name=$value"
}
