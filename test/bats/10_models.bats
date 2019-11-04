#!/usr/bin/env bats

setup () {
    load tancredi_client
}

@test "Create new model" {
    run POST /tancredi/api/v1/models <<EOF
{
    "name": "acme19_2",
    "display_name": "Acme IP phone v19 rev. 2",
    "variables": {
        "var1": "value1",
        "var2": "value2"
    }
}
EOF
    assert_http_code "201"
}

@test "Delete existing free model" {
    run DELETE /tancredi/api/v1/models/acme19_2
    assert_http_code "204"
}

@test "Re-create new model after delete" {
    run POST /tancredi/api/v1/models <<EOF
{
    "name": "acme19_2",
    "display_name": "Acme IP phone v19 rev. 2",
    "variables": {
        "var1": "value1",
        "var2": "value2"
    }
}
EOF
    assert_http_code "201"
    assert_http_header "Location" "/tancredi/api/v1/models/acme19_2"
}

@test "Get the new model" {
    run GET /tancredi/api/v1/models/acme19_2
    assert_http_code "200"
    assert_http_body '"name":"acme19_2"'
    assert_http_body '"var1":"value1"'
}