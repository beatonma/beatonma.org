#!/usr/bin/env ash

# This script should be configured to run at least once per hour.

logmsg() {
  echo "`date "+%Y/%m/%d-%H:%M:%S"` $@"
}

logmsg "Heartbeat tick"
