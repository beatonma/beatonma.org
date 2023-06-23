#!/usr/bin/env bash

# Make node_modules accessible
ln -s /usr/local/lib/node_modules ./node_modules

cypress run

rm ./node_modules
