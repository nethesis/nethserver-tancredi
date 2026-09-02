#!/usr/bin/env php
<?php

/*
 * Copyright (C) 2026 Nethesis S.r.l.
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

function usage($script)
{
    fwrite(STDERR, "Usage: {$script} prepare-tokens | set-host <new-nethvoice-host>\n");
    exit(2);
}

if ($argc < 2) {
    usage($argv[0]);
}

$action = $argv[1];
if (($action === 'prepare-tokens' && $argc !== 2)
    || ($action === 'set-host' && $argc !== 3)
    || ($action !== 'prepare-tokens' && $action !== 'set-host')
) {
    usage($argv[0]);
}

if ($action === 'set-host') {
    $hostname = $argv[2];
    if (strpos($hostname, '.') === false
        || filter_var($hostname, FILTER_VALIDATE_DOMAIN, FILTER_FLAG_HOSTNAME) === false
    ) {
        fwrite(STDERR, "Invalid NethVoice host: {$hostname}\n");
        exit(2);
    }
}

require_once __DIR__.'/../vendor/autoload.php';
require_once __DIR__.'/../src/init.php';

$storage = new \Tancredi\Entity\FileStorage(null, $config);

if ($action === 'set-host') {
    $defaults = new \Tancredi\Entity\Scope('defaults', $storage, null);
    if (!$defaults->setVariables(array('hostname' => $hostname))) {
        fwrite(STDERR, "Cannot update the Tancredi default hostname\n");
        exit(1);
    }
    printf("Tancredi provisioning host changed to %s\n", $hostname);
    exit(0);
}

$phones = $storage->listScopes('phone');
sort($phones, SORT_STRING);
$journalPath = rtrim($config['rw_dir'], '/').'/.ns8-migration-tokens.json';
$tokenPlan = array();

if (file_exists($journalPath)) {
    $journal = json_decode(file_get_contents($journalPath), true);
    if (!is_array($journal)
        || !isset($journal['version'], $journal['phones'])
        || $journal['version'] !== 1
        || !is_array($journal['phones'])
    ) {
        fwrite(STDERR, "Invalid NS8 token migration journal: {$journalPath}\n");
        exit(1);
    }
    $journalPhones = array_keys($journal['phones']);
    sort($journalPhones, SORT_STRING);
    if ($journalPhones !== $phones) {
        fwrite(STDERR, "Tancredi phone set changed after NS8 token preparation\n");
        exit(1);
    }
    foreach ($journal['phones'] as $mac => $tokens) {
        if (!is_array($tokens)
            || empty($tokens['tok1'])
            || empty($tokens['tok2'])
            || $tokens['tok1'] === $tokens['tok2']
        ) {
            fwrite(STDERR, "Invalid token plan for phone {$mac}\n");
            exit(1);
        }
    }
    $tokenPlan = $journal['phones'];
} else {
    $usedTokens = array();

    // Validate the complete phone set before creating the journal or tokens.
    foreach ($phones as $mac) {
        $tok1 = \Tancredi\Entity\TokenManager::getToken1($mac);
        $tok2 = \Tancredi\Entity\TokenManager::getToken2($mac);
        if (empty($tok2)) {
            fwrite(STDERR, "Missing tok2 for phone {$mac}\n");
            exit(1);
        }
        if (!empty($tok1)) {
            $usedTokens[$tok1] = true;
        }
        $usedTokens[$tok2] = true;
        $tokenPlan[$mac] = array('tok1' => $tok2, 'tok2' => null);
    }

    foreach ($tokenPlan as $mac => $tokens) {
        do {
            // Use the same token generation method as the legacy Tancredi API.
            $newToken = str_replace('.', '', uniqid((string) rand(), true));
        } while (isset($usedTokens[$newToken]));
        $usedTokens[$newToken] = true;
        $tokenPlan[$mac]['tok2'] = $newToken;
    }

    $journal = json_encode(
        array('version' => 1, 'phones' => $tokenPlan),
        JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES
    );
    if ($journal === false) {
        fwrite(STDERR, "Cannot encode the NS8 token migration journal\n");
        exit(1);
    }
    $journalTmp = tempnam($config['rw_dir'], '.ns8-migration-tokens.');
    if ($journalTmp === false
        || file_put_contents($journalTmp, $journal."\n", LOCK_EX) === false
        || !chmod($journalTmp, 0600)
        || !rename($journalTmp, $journalPath)
    ) {
        if ($journalTmp !== false && file_exists($journalTmp)) {
            unlink($journalTmp);
        }
        fwrite(STDERR, "Cannot write the NS8 token migration journal\n");
        exit(1);
    }
}

foreach ($tokenPlan as $mac => $tokens) {
    if (\Tancredi\Entity\TokenManager::createToken($tokens['tok1'], $mac, true) === false
        || \Tancredi\Entity\TokenManager::createToken($tokens['tok2'], $mac, false) === false
    ) {
        fwrite(STDERR, "Cannot prepare migration tokens for phone {$mac}\n");
        exit(1);
    }
}

printf("Tancredi migration tokens prepared for %d phone(s)\n", count($phones));
