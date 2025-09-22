#!/bin/bash

# Determine script and project directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# If script is in root (current behavior), use current directory
if [[ "$(basename "$SCRIPT_DIR")" != "scripts" ]]; then
    PROJECT_ROOT="$SCRIPT_DIR"
fi

# Function to handle script interruption for graceful shutdown
cleanup_and_exit() {
    echo -e "\nCaught Ctrl+C. Shutting down the task runner."
    exit 0
}

# Trap SIGINT (Ctrl+C) to ensure the script exits cleanly
trap cleanup_and_exit SIGINT

# Function to execute a task with retry logic
execute_task() {
    local task_file="$1"
    local max_retries=3
    local attempt=1

    # Read task content
    task_content=$(cat "$task_file")

    # Create log file path
    local log_file="$PROJECT_ROOT/tasks/logs/$(basename "$task_file")"

    # Initialize log file with task prompt if it doesn't exist
    if [ ! -f "$log_file" ]; then
        echo "Creating log file for task: $(basename "$task_file")"
        # Ensure logs directory exists
        mkdir -p "$PROJECT_ROOT/tasks/logs"
        # Copy task prompt to log file
        cp "$task_file" "$log_file"
    fi

    while [ $attempt -le $max_retries ]; do
        echo "Attempt $attempt of $max_retries for task: $(basename "$task_file")"

        # Create temporary file for output
        local temp_output=$(mktemp)

        # Add attempt header to log
        echo "" >> "$log_file"
        echo "=== EXECUTION ATTEMPT $attempt ===" >> "$log_file"
        echo "Started at: $(date)" >> "$log_file"
        echo "" >> "$log_file"

        # Run the command with task content as query
        if claude -p "$task_content" --permission-mode acceptEdits > "$temp_output" 2>&1; then
            echo "Task completed successfully on attempt $attempt"

            # Append success result to log file
            echo "=== EXECUTION RESULT (SUCCESS) ===" >> "$log_file"
            echo "Completed at: $(date)" >> "$log_file"
            echo "Attempt: $attempt" >> "$log_file"
            echo "" >> "$log_file"
            cat "$temp_output" >> "$log_file"

            # Remove task from pending folder after successful completion
            rm "$task_file"

            # Clean up temp file
            rm "$temp_output"
            return 0
        else
            echo "Task failed on attempt $attempt"

            # Append failure result to log file
            echo "=== EXECUTION RESULT (FAILURE) ===" >> "$log_file"
            echo "Failed at: $(date)" >> "$log_file"
            echo "Attempt: $attempt" >> "$log_file"
            echo "" >> "$log_file"
            cat "$temp_output" >> "$log_file"

            attempt=$((attempt + 1))

            if [ $attempt -le $max_retries ]; then
                echo "Retrying in 30 seconds..."
                sleep 30
            fi
        fi

        # Clean up temp file
        rm "$temp_output"
    done

    echo "Task failed after $max_retries attempts. Skipping..."
    echo "" >> "$log_file"
    echo "=== FINAL STATUS ===" >> "$log_file"
    echo "Task failed after $max_retries attempts at: $(date)" >> "$log_file"
    return 1
}

# Check if delay argument is provided
if [ $# -gt 0 ]; then
    delay_minutes=$1
    delay_seconds=$((delay_minutes * 60))
    echo "Initial delay: $delay_minutes minutes ($delay_seconds seconds)"
    echo "First run will start at $(date -d "+$delay_minutes minutes")"
    sleep $delay_seconds
fi

while true; do
    # Record cycle start time after any delay
    cycle_start=$(date +%s)
    echo "Checking for tasks at $(date)..."

    # Check if there are any pending tasks
    for task_file in "$PROJECT_ROOT"/tasks/pending/*.md; do
        echo "Processing task: $(basename "$task_file")"

        # Execute task with retry logic
        execute_task "$task_file"

        if [ $? -ne 0 ]; then
          break
        fi
    done

    echo "Execution cycle finished. Waiting for 5 hours..."

    # Calculate accurate sleep time: start + 5 hours - current time
    current_time=$(date +%s)
    next_cycle_time=$((cycle_start + 18000)) # 5 hours = 18000 seconds
    sleep_time=$((next_cycle_time - current_time))

    if [ $sleep_time -gt 0 ]; then
        echo "Sleeping for $sleep_time seconds (next cycle at $(date -d "@$next_cycle_time"))"
        sleep $sleep_time
    else
        echo "Execution took longer than 5 hours, starting next cycle immediately"
    fi
done
