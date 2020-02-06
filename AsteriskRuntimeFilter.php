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
        // Get account index
        $indexes = array();
        foreach (array_keys($variables) as $key) {
            if (strpos('account_username_', $key)) {
                $indexes[] = str_replace('account_username_','',$key);
            }
        }
        if (empty($indexes)) $indexes[] = 1;

        foreach ($indexes as $index) {
            if (!empty($variables['mainextension_'.$index])) {
                $extension = $variables['mainextension_'.$index];
            } elseif (!empty($variables['extension_'.$index])) {
                $extension = $variables['extension_'.$index];
            } elseif (!empty($variables['account_username_'.$index])) {
                $extension = $variables['account_username_'.$index];
            } else {
                return $variables;
            }

            $statement = $this->db->prepare('SELECT key,value FROM astdb WHERE key LIKE :key');
            $statement->bindValue(':key', "%/$extension%");

            $results = $statement->execute();

            $variables['call_waiting'] = 0;
            $variables['dnd_enable'] = 0;
            while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
                if ($row['key'] == "/CW/$extension" && $row['value'] == 'ENABLED') {
                    $variables['call_waiting_'.$index] = 1;
                }

                if ($row['key'] == "/CFU/$extension") {
                    $variables['timeout_fwd_target_'.$index] = $row['value'];
                    $variables['timeout_fwd_enable_'.$index] = (int) !empty($row['value']);
                }

                if ($row['key'] == "/CFB/$extension") {
                    $variables['busy_fwd_target_'.$index] = $row['value'];
                    $variables['busy_fwd_enable_'.$index] = (int) !empty($row['value']);
                }

                if ($row['key'] == "/CF/$extension") {
                    $variables['always_fwd_target_'.$index] = $row['value'];
                    $variables['always_fwd_enable_'.$index] = (int) !empty($row['value']);
                }

                if ($row['key'] == "/AMPUSER/$extension/followme/prering") {
                    $variables['cftimeout_'.$index] = $row['value'];
                }

                if ($row['key'] == "/DND/$extension" && $row['value'] == 'YES') {
                    $variables['dnd_enable_'.$index] = 1;
                }
            }
        }
        $this->logger->debug(__CLASS__ . "Added runtime variables");
        $this->db->close();
        return $variables;
    }
}

