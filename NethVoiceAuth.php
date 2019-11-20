<?php namespace Tancredi\Entity;

class NethVoiceAuth
{
    private $config;

    /**
     * @throws \RuntimeException
     */
    public function __construct($config)
    {
        if ( ! is_array($config)
            || ! $config['secret']
            || ! $config['static_token']
            ) {
            throw new \RuntimeException('Bad NethVoiceAuth configuration', 1574245361);
        }
        $this->config = $config;
    }

    public function __invoke($request, $response, $next)
    {
        if ($request->isOptions()) {
            $response = $next($request, $response);
        } elseif ($request->hasHeader('Authentication')) {
            if($request->getHeaderLine('Authentication') === ('static ' . $this->config['static_token'])
                && ($request->getHeaderLine('HTTP_HOST') === '127.0.0.1' || $request->getHeaderLine('HTTP_HOST') === 'localhost')
            ) {
                // Local autentication for NethCTI success
                $response = $next($request, $response);
            } else {
                $results = array(
                    'type' => 'https://nethesis.github.io/tancredi/problems#forbidden',
                    'title' => 'Access to resource is forbidden with current client privileges',
                    'detail' => 'Invalid client credentials'
                );
                $response = $response->withJson($results, 403);
                $response = $response->withHeader('Content-Type', 'application/problem+json');
                $response = $response->withHeader('Content-Language', 'en');
            }
        } elseif ($request->hasHeader('Secretkey') && $request->hasHeader('User')) {
            $dbh = new \PDO(
                'mysql:dbname=asterisk;host=localhost',
                'tancredi',
                $this->config['auth_nethvoice_dbpass']
            );
            $stmt = $dbh->prepare("SELECT * FROM ampusers WHERE sections LIKE '%*%' AND username = ?");
            $stmt->execute(array($request->getHeaderLine('User')));
            $user = $stmt->fetchAll();
            $password_sha1 = $user[0]['password_sha1'];
            $username = $user[0]['username'];

            // check the user is valid and is an admin (sections = *)
            if (isset($username, $password_sha1) && $request->getHeaderLine('Secretkey') === sha1($username . $password_sha1 . $this->config['secret'])) {
                $response = $next($request, $response);
            } else {
                $results = array(
                    'type' => 'https://nethesis.github.io/tancredi/problems#forbidden',
                    'title' => 'Access to resource is forbidden with current client privileges',
                    'detail' => 'Invalid client credentials'
                );
                $response = $response->withJson($results, 403);
                $response = $response->withHeader('Content-Type', 'application/problem+json');
                $response = $response->withHeader('Content-Language', 'en');
            }
        } else {
            $results = array(
                'type' => 'https://nethesis.github.io/tancredi/problems#forbidden',
                'title' => 'Access to resource is forbidden with current client privileges',
                'detail' => 'Invalid NethVoiceAuth authentication headers',
            );
            $response = $response->withJson($results, 403);
            $response = $response->withHeader('Content-Type', 'application/problem+json');
            $response = $response->withHeader('Content-Language', 'en');
        }
        return $response;
    }
}

