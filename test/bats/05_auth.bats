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

@test "Authenticated GET /models" {
    local secret tancrediDBPass User fpbxPasswordHash SecretKey
    secret=$(perl -mNethServer::Password -e "print NethServer::Password::store('nethvoice')")
    tancrediDBPass=$(perl -mNethServer::Password -e "print NethServer::Password::store('TancrediDBPass')")
    User="admin"
    if [[ -x /usr/bin/mysql ]]; then
        fpbxPasswordHash=$(mysql asterisk -utancredi -p$tancrediDBPass -B --silent -e "SELECT password_sha1 FROM ampusers WHERE username = '$User'")
    fi
    SecretKey=$(echo -n "${User}${fpbxPasswordHash}${secret}" | sha1sum | awk '{print $1}')

    run GET -H "User: ${User}" -H "SecretKey: ${SecretKey}" /tancredi/api/v1/models
    assert_http_code "200"
}

@test "Authenticated GET /models (failed/forbidden)" {
    run GET -H "User: expect-fail" -H "SecretKey: expect-fail" /tancredi/api/v1/models
    assert_http_code "403"
    assert_http_body "problems#forbidden"
    assert_http_body "problems#forbidden"
}

@test "Bypass authentication from now on..." {
    # Disable authentication class for subsequent steps
    sed -i 's/^auth_class/#auth_class/' /etc/tancredi.conf
    skip
}
