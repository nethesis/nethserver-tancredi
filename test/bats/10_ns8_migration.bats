#!/usr/bin/env bats

#
# Copyright (C) 2026 Nethesis S.r.l.
# SPDX-License-Identifier: GPL-3.0-or-later
#

setup() {
    test_root=$(mktemp -d)
    mkdir -p \
        "$test_root/ro/scopes" \
        "$test_root/rw/scopes" \
        "$test_root/rw/first_access_tokens" \
        "$test_root/rw/tokens"

    cat > "$test_root/tancredi.conf" <<EOF
[config]
logfile = ""
loglevel = "ERROR"
ro_dir = "$test_root/ro/"
rw_dir = "$test_root/rw/"
EOF

    cat > "$test_root/rw/scopes/defaults.ini" <<'EOF'
[metadata]
scopeType = "defaults"

[data]
hostname = "old.example.org"
EOF

    cat > "$test_root/rw/scopes/AA-BB-CC-DD-EE-FF.ini" <<'EOF'
[metadata]
scopeType = "phone"
inheritFrom = "yealink-T46"
displayName = "Test phone"

[data]
EOF

    printf 'AA-BB-CC-DD-EE-FF' > "$test_root/rw/tokens/migrated-token"
    printf 'AA-BB-CC-DD-EE-FF' > "$test_root/rw/first_access_tokens/old-token"
}

teardown() {
    rm -rf "$test_root"
}

run_helper() {
    helper=${TANCREDI_NS8_MIGRATION_HELPER:-/usr/share/tancredi/scripts/ns8-migration.php}
    if [[ -x /usr/bin/scl ]]; then
        env tancredi_conf="$test_root/tancredi.conf" \
            /usr/bin/scl enable rh-php73 -- \
            php "$helper" "$@"
    else
        env tancredi_conf="$test_root/tancredi.conf" php "$helper" "$@"
    fi
}

@test "prepare a new tok2 and reuse the migrated tok2 as tok1" {
    run run_helper prepare-tokens

    [ "$status" -eq 0 ]
    grep -q '^hostname = "old.example.org"$' "$test_root/rw/scopes/defaults.ini"
    [ ! -e "$test_root/rw/first_access_tokens/old-token" ]
    [ "$(cat "$test_root/rw/first_access_tokens/migrated-token")" = "AA-BB-CC-DD-EE-FF" ]
    [ ! -e "$test_root/rw/tokens/migrated-token" ]
    [ "$(find "$test_root/rw/tokens" -type f | wc -l)" -eq 1 ]
    [ "$(stat -c '%a' "$test_root/rw/.ns8-migration-tokens.json")" = "600" ]
}

@test "token preparation is idempotent" {
    run run_helper prepare-tokens
    [ "$status" -eq 0 ]
    new_token=$(basename "$(find "$test_root/rw/tokens" -type f)")

    # Simulate a phone completing the first stage on legacy Tancredi.
    rm "$test_root/rw/first_access_tokens/migrated-token"

    run run_helper prepare-tokens
    [ "$status" -eq 0 ]
    [ -e "$test_root/rw/first_access_tokens/migrated-token" ]
    [ -e "$test_root/rw/tokens/$new_token" ]
    [ "$(find "$test_root/rw/first_access_tokens" -type f | wc -l)" -eq 1 ]
    [ "$(find "$test_root/rw/tokens" -type f | wc -l)" -eq 1 ]
}

@test "change only the default provisioning host after preparation" {
    run run_helper prepare-tokens
    [ "$status" -eq 0 ]
    token_files_before=$(find "$test_root/rw/first_access_tokens" "$test_root/rw/tokens" -type f -printf '%P\n' | sort)

    run run_helper set-host voice.example.org

    [ "$status" -eq 0 ]
    grep -q '^hostname = "voice.example.org"$' "$test_root/rw/scopes/defaults.ini"
    token_files_after=$(find "$test_root/rw/first_access_tokens" "$test_root/rw/tokens" -type f -printf '%P\n' | sort)
    [ "$token_files_after" = "$token_files_before" ]
}

@test "reject an invalid host before changing data" {
    run run_helper set-host invalid-host

    [ "$status" -eq 2 ]
    grep -q '^hostname = "old.example.org"$' "$test_root/rw/scopes/defaults.ini"
    [ -e "$test_root/rw/first_access_tokens/old-token" ]
}

@test "reject a phone without tok2 before changing data" {
    rm "$test_root/rw/tokens/migrated-token"

    run run_helper prepare-tokens

    [ "$status" -eq 1 ]
    grep -q '^hostname = "old.example.org"$' "$test_root/rw/scopes/defaults.ini"
    [ -e "$test_root/rw/first_access_tokens/old-token" ]
    [ ! -e "$test_root/rw/.ns8-migration-tokens.json" ]
}
