#!/usr/bin/env bash

NOOP_MODE=0
NOOP_PATH="/tmp/no-op"


log() {
  echo "$*" > "$(tty)"
}

if [ "$1" = "noop" ]; then
  NOOP_MODE=1
  shift
  if [ ! -d "$NOOP_PATH" ]; then
    mkdir "$NOOP_PATH"
  fi
  log "no-op mode enabled:"
  log "- Commands will not be executed"
  log "- File paths will be redirected to $NOOP_PATH"
  log ""
fi

error() {
  log "  ERROR: $*"
}

rootpath() {
  if [ $NOOP_MODE = 1 ]; then
    noop_path="${NOOP_PATH}$1"
    if [[ "$(basename "$noop_path")" == *"."* ]]; then
      # Assume basename with a . is meant to be a filename.
      mkdir -p "$(dirname "$noop_path")"
    else
      mkdir -p "$noop_path"
    fi
    echo "$noop_path"
  else
    echo "$1"
  fi
}

run_command() {
  log "COMMAND: $*"

  if [ $NOOP_MODE = 1 ]; then
    log "NOOP: $*"
  else
    if ! eval "$@"; then
      exit 1
    fi
  fi
}

apt_install() {
  run_command "sudo apt install -y $*"
}

subscript() {
  log "SCRIPT: $*"
  if ! bash "$@"; then
    error "SCRIPT ERROR"
    exit 1
  fi
  read -n 1 -p "Continue?"
  log ''
}


: "
Exported functions
"
export -f apt_install
export -f error
export -f log
export -f rootpath
export -f run_command
export -f subscript
