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
        -v -X ${verb} "${@}" "${tancredi_base_url}${path}" 2>&1
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
    grep -q -E "^< HTTP/1\\.1 $1" <<<"$output"
}

assert_http_header () {
    grep -q -F "< ${1}: ${2}" <<<"$output"
}

assert_http_body () {
    sed -n '$ p' <<<"$output" | grep -q -F $1
}