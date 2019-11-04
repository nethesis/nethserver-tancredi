#!/bin/bash

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