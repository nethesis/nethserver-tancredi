<?php namespace Tancredi\Entity;

/*
* AsteriskRuntimeFilter class add astdb variables to scope data
*
* call_waiting: call waiting status (1|0)
* dnd_enable: do not disturb status (1|0)
* timeout_fwd_enable: call forward on timeout status (1|0)
* timeout_fwd_target: call forward on timeout target (phone number)
* busy_fwd_enable: call forward on busy status (1|0)
* busy_fwd_target: call forward on busy target (phone number)
* always_fwd_enable: call forward always on status (1|0)
* always_fwd_target: call forward always on  target (phone number)
* cftimeout: call forward timeout
*/
class AsteriskRuntimeFilter
{
    private $db;
    private $logger;

    public function __construct($config,$logger)
    {
        $this->db = new \SQLite3($config['astdb'],SQLITE3_OPEN_READONLY);
        $this->logger = $logger;
    }

    public function __invoke($variables)
    {
        foreach (array_keys($variables) as $variable) {
            if(substr($variable, 0, 18) != 'account_extension_') {
                // Ignore all variables except those starting with "account_extension_"
                continue;
            }

            $index = (integer) substr($variable, 18);
            if($index <= 0) {
                // index must be a positive integer
                continue;
            }

            // Initialize default values
            $variables['account_call_waiting_' . $index] = '';
            $variables['account_timeout_fwd_target_' . $index] = '';
            $variables['account_busy_fwd_target_' . $index] = '';
            $variables['account_always_fwd_target_' . $index] = '';
            $variables['account_cftimeout_' . $index] = '';
            $variables['account_dnd_enable_' . $index] = '';

            $mainextension_match = array();
            $extension = $variables[$variable];
            if(preg_match("/^9\d(\d\d\d)$/", $extension, $mainextension_match)) {
                $extension = $mainextension_match[1];
            }

            $statement = $this->db->prepare('SELECT key,value FROM astdb WHERE key LIKE :key');
            $statement->bindValue(':key', "%/$extension%");
            $results = $statement->execute();

            while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
                if ($row['key'] == "/CW/$extension" && $row['value'] == 'ENABLED') {
                    $variables['account_call_waiting_' . $index] = '1';
                } 

                if ($row['key'] == "/CFU/$extension") {
                    $variables['account_timeout_fwd_target_' . $index] = $row['value'];
                }

                if ($row['key'] == "/CFB/$extension") {
                    $variables['account_busy_fwd_target_' . $index] = $row['value'];
                }

                if ($row['key'] == "/CF/$extension") {
                    $variables['account_always_fwd_target_' . $index] = $row['value'];
                }

                if ($row['key'] == "/AMPUSER/$extension/followme/prering") {
                    $variables['account_cftimeout_' . $index] = $row['value'];
                }

                if ($row['key'] == "/DND/$extension" && $row['value'] == 'YES') {
                    $variables['account_dnd_enable_' . $index] = '1';
                }
            }
        }
        return $variables;
    }
}

