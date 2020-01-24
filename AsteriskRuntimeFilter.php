<?php namespace Tancredi\Entity;

class AsteriskRuntimeFilter
{
    private $db;
    private $logger;
    /**
     * @throws \RuntimeException
     */
    public function __construct($config,$logger)
    {
        $this->db = new \SQLite3($config['astdb'],SQLITE3_OPEN_READONLY);
        $this->logger = $logger;
    }

    public function __invoke($variables)
    {
        if (!empty($variables['mainextension'])) {
            $extension = $variables['mainextension'];
        } elseif (!empty($variables['extension'])) {
            $extension = $variables['extension'];
        } elseif (!empty($variables['username'])) {
            $extension = $variables['username'];
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
                $variables['call_waiting'] = 1;
            }

            if ($row['key'] == "/CFU/$extension") {
                $variables['timeout_fwd_target'] = $row['value'];
                $variables['timeout_fwd_enable'] = (int) !empty($row['value']);
            }

            if ($row['key'] == "/CFB/$extension") {
                $variables['busy_fwd_target'] = $row['value'];
                $variables['busy_fwd_enable'] = (int) !empty($row['value']);
            }

            if ($row['key'] == "/CF/$extension") {
                $variables['always_fwd_target'] = $row['value'];
                $variables['always_fwd_enable'] = (int) !empty($row['value']);
            }

            if ($row['key'] == "/AMPUSER/$extension/followme/prering") {
                $variables['cftimeout'] = $row['value'];
            }

            if ($row['key'] == "/DND/$extension" && $row['value'] == 'YES') {
                $variables['dnd_enable'] = 1;
            }
        }
        $this->logger->debug(__CLASS__ . "Added runtime variables");
        $this->db->close();
        return $variables;
    }
}

