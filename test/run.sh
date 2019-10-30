#!/usr/bin/bash

if ! which bats &>/dev/null; then
    yum --enablerepo=epel install bats
fi

bats bats/
