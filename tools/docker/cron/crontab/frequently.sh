#!/usr/bin/env ash

# This script should be configured to run at least once per hour.

logmsg() {
  echo "`date "+%Y/%m/%d-%H:%M:%S"` $@"
}

run_task() {
  # Run the given Django management command after a random delay.
  sleep $((RANDOM % 60))
  logmsg "Running task '$@'"
  python /django/manage.py "$@"
}

logmsg "Frequent tasks starting..."
run_task update_github_events
logmsg "Frequent tasks complete."
