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
      -s -i \
      -H 'Accept: application/json, application/problem+json' \
      -X "${verb}" "${@}" "${tancredi_base_url}${path}"
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
    if ! grep -q -F "HTTP/1.1 $1" <<<"${lines[0]}"; then
        echo "${lines[0]}" 1>&2
        return 1
    fi
    return 0
}

assert_http_header () {
    sed '/^$/q' <<<"$output" | grep -q -F "${1}: ${2}" || :
    if [[ ${PIPESTATUS[1]} != 0 ]]; then
        return 1
    fi
    return 0
}

assert_http_body () {
    sed -n -r '/^\s*$/,$ p' <<<"$output" | grep -q -F "$1" || :
    if [[ ${PIPESTATUS[1]} != 0 ]]; then
        sed -n '$ p' <<<"$output" 1>&2
        return 1
    fi
    return 0
}

assert_http_body_re () {
    sed -n -r '/^\s*$/,$ p' <<<"$output" | grep -q -E "$1" || :
    if [[ ${PIPESTATUS[1]} != 0 ]]; then
        sed -n '$ p' <<<"$output" 1>&2
        return 1
    fi
    return 0
}

assert_http_body_empty () {
    sed -n -r '/^\s*$/,$ p' <<<"$output" | grep -E '\w' || :
    if [[ ${PIPESTATUS[1]} == 0 ]]; then
        return 1
    fi
    return 0
}
