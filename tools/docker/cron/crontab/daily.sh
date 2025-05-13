#!/usr/bin/env ash

# This script should be configured to run once per day.

logmsg() {
  echo "`date "+%Y/%m/%d-%H:%M:%S"` $@"
}

run_task() {
  # Run the given Django management command after a random delay.
  sleep $((RANDOM % 60))
  logmsg "Running task '$@'"
  python /django/manage.py "$@"
}

logmsg "No daily tasks registered"
