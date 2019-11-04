#!/usr/bin/env bats

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

setup () {
    load tancredi_client
}

@test "Reset storage dir" {
    find /var/lib/tancredi -type f -delete
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
    assert_http_header "Location" "/tancredi/api/v1/models/acme19_2"
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
