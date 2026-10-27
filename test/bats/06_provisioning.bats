#!/usr/bin/env bats

setup () {
    load tancredi_client
}

@test "Tokenless provisioning is forbidden even from localhost" {
    local filename
    for filename in 001565123456.cfg cfg001565123456.xml 001565123456.htm 'custom+phone.cfg'; do
        run GET "/provisioning/${filename}"
        assert_http_code "403"
    done
}

@test "Token provisioning and asset requests still reach Tancredi" {
    local path
    for path in 001565123456.cfg firmware/missing.bin backgrounds/missing.png ringtones/missing.wav screensavers/missing.png; do
        run GET "/provisioning/invalid-regression-test-token/${path}"
        assert_http_code "404"
    done
}

@test "Provisioning health check remains available" {
    run GET /provisioning/check/ping
    assert_http_code "200"
}
