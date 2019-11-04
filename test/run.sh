#!/bin/bash

if ! which bats &>/dev/null; then
    echo "The bats command is missing. You can install it with:"
    echo "    yum --enablerepo=epel install bats"
    exit 1
fi

bats bats/
