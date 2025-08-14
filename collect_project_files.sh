#!/bin/bash

# Script to collect contents of all relevant Django project files into a single text document

# Use current directory as project directory by default, or allow override
PROJECT_DIR="${1:-$(pwd)}"
OUTPUT_FILE="$HOME/project_files_output.txt"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %Z')

# Ensure project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
  echo "Error: Project directory $PROJECT_DIR does not exist."
  exit 1
fi

# Initialize or clear the output file
echo "Django Project Files Collection - $TIMESTAMP" > "$OUTPUT_FILE"
echo "===========================================" >> "$OUTPUT_FILE"
echo "Project Directory: $PROJECT_DIR" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Function to append file content to output
append_file_content() {
  local file_path="$1"
  if [ -f "$file_path" ]; then
    echo "===== $file_path =====" >> "$OUTPUT_FILE"
    cat "$file_path" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "----------------------------------------" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
  else
    echo "===== $file_path =====" >> "$OUTPUT_FILE"
    echo "File not found" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "----------------------------------------" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
  fi
}

# Change to project directory
cd "$PROJECT_DIR" || exit 1

# List of specific files to collect
SPECIFIC_FILES=(
  "apps/facilities/models.py"
  "facility_project/facilities/models.py"
  "apps/facilities/serializers.py"
  "facility_project/facilities/serializers.py"
  "apps/facilities/views.py"
  "facility_project/facilities/views.py"
  "apps/api/urls.py"
  "facility_project/urls.py"
  "apps/facilities/urls.py"
  "facility_project/facilities/urls.py"
  "apps/settings.py"
  "facility_project/settings.py"
  "manage.py"
  "facility_project/manage.py"
  "requirements.txt"
  "apps/common/models.py"
)

# List of directories to search for Python files
PYTHON_DIRS=(
  "apps/facilities"
  "facility_project/facilities"
  "apps/api"
  "apps/common"
  "facility_project"
)

# List of management command directories
COMMAND_DIRS=(
  "apps/facilities/management/commands"
  "facility_project/facilities/management/commands"
)

# List of migration directories
MIGRATIONS_DIRS=(
  "apps/facilities/migrations"
  "facility_project/facilities/migrations"
)

# Append contents of specific files
echo "===== SPECIFIC FILES =====" >> "$OUTPUT_FILE"
for file in "${SPECIFIC_FILES[@]}"; do
  append_file_content "$file"
done

# Append contents of Python files in specified directories
for dir in "${PYTHON_DIRS[@]}"; do
  if [ -d "$dir" ]; then
    echo "===== Python Files in $dir =====" >> "$OUTPUT_FILE"
    find "$dir" -type f -name "*.py" ! -name "__init__.py" -exec sh -c '
      file="{}"
      echo "----- $file -----" >> '"$OUTPUT_FILE"'
      cat "$file" >> '"$OUTPUT_FILE"'
      echo "" >> '"$OUTPUT_FILE"'
      echo "----------------------------------------" >> '"$OUTPUT_FILE"'
      echo "" >> '"$OUTPUT_FILE"'
    ' \;
  else
    echo "===== $dir =====" >> "$OUTPUT_FILE"
    echo "Directory not found" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "----------------------------------------" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
  fi
done

# Append contents of management command files
for dir in "${COMMAND_DIRS[@]}"; do
  if [ -d "$dir" ]; then
    echo "===== Management Command Files in $dir =====" >> "$OUTPUT_FILE"
    find "$dir" -type f -name "*.py" ! -name "__init__.py" -exec sh -c '
      file="{}"
      echo "----- $file -----" >> '"$OUTPUT_FILE"'
      cat "$file" >> '"$OUTPUT_FILE"'
      echo "" >> '"$OUTPUT_FILE"'
      echo "----------------------------------------" >> '"$OUTPUT_FILE"'
      echo "" >> '"$OUTPUT_FILE"'
    ' \;
  else
    echo "===== $dir =====" >> "$OUTPUT_FILE"
    echo "Directory not found" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "----------------------------------------" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
  fi
done

# Append contents of migration files
for dir in "${MIGRATIONS_DIRS[@]}"; do
  if [ -d "$dir" ]; then
    echo "===== Migration Files in $dir =====" >> "$OUTPUT_FILE"
    find "$dir" -type f -name "*.py" ! -name "__init__.py" -exec sh -c '
      file="{}"
      echo "----- $file -----" >> '"$OUTPUT_FILE"'
      cat "$file" >> '"$OUTPUT_FILE"'
      echo "" >> '"$OUTPUT_FILE"'
      echo "----------------------------------------" >> '"$OUTPUT_FILE"'
      echo "" >> '"$OUTPUT_FILE"'
    ' \;
  else
    echo "===== $dir =====" >> "$OUTPUT_FILE"
    echo "Directory not found" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "----------------------------------------" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
  fi
done

echo "File collection complete. Output saved to $OUTPUT_FILE"
echo "Total files processed: $(grep -c "=====" "$OUTPUT_FILE")"