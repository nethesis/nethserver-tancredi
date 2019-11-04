#!/bin/bash

#
# Copyright (C) 2019 Nethesis S.r.l.
# http://www.nethesis.it - nethserver@nethesis.it
#
# This script is part of NethServer.
#
# NethServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# NethServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NethServer.  If not, see COPYING.
#

tancredi_base_url=http://127.0.0.1

xcurl () {
    local verb
    verb=$1
    shift
    path=$1
    shift
    curl \
        -H 'Accept: application/json, application/problem+json' \
        -v -X ${verb} "${@}" "${tancredi_base_url}${path}"
}

GET () {
    xcurl GET "$1"
}


DELETE () {
    xcurl DELETE "$1"
}

POST () {
    xcurl POST $1 \
        -d @- -H 'Content-Type: application/json'
}

PATCH () {
    xcurl PATCH $1 \
        -d @- -H 'Content-Type: application/json'
}

assert_http_code () {
    if ! grep -q -E "^< HTTP/1\\.1 $1" <<<"$output"; then
        grep -E "^<" <<<"$output" 1>&2
        return 1
    fi
}

assert_http_header () {
    if ! grep -q -F "< ${1}: ${2}" <<<"$output"; then
        grep -E "^<" <<<"$output" 1>&2
        return 1
    fi
}

assert_http_body () {
    sed -n '$ p' <<<"$output" | grep -q -F $1
    if [[ $? != 0 ]]; then
        grep -E "^{" <<<"$output" 1>&2
        return 1
    fi
}
