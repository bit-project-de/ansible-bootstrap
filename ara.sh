#!/bin/bash

env_vars=$(python -m ara.setup.env)
eval "$env_vars"

SCRIPT_PATH=$(dirname $(realpath -s $0))

export ARA_DIR="${SCRIPT_PATH}/.ara"
export ARA_DATABASE="sqlite:///${ARA_DIR}/ansible.sqlite"

$@
