<?php namespace Tancredi\Entity;

class NethVoiceAuth
{
    private $config;

    public function __construct($config) {
        if (!is_array($config) or !array_key_exists('secret',$config) or !array_key_exists('static_token',$config)) {
            throw new RuntimeException('Wrong or missing configuration');
        }
        $this->config = $config;
    }

    public function __invoke($request, $response, $next)
    {
        if ($request->isOptions()) {
            $response = $next($request, $response);
        } elseif ($request->hasHeader('Authentication:Static') and !empty($this->config['static_token']) and ($request->getHeaderLine('HTTP_HOST') === '127.0.0.1' or $request->getHeaderLine('HTTP_HOST') === 'localhost') and $request->getHeaderLine('Authentication:Static') === $this->config['static_token']) {
            // Local autentication for NethCTI success
            $response = $next($request, $response);
	} elseif ($request->hasHeader('Secretkey') and !empty($this->config['secret'])) {
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

            # check the user is valid and is an admin (sections = *)
            if (!$username) {
                return $response->withJson(['error' => 'Forbidden: invalid user'], 403);
            }
            $hash = sha1($username . $password_sha1 . $this->config['secret']);
            if ($request->getHeaderLine('Secretkey') != $hash) {
                $results = array(
                    'type' => 'https://nethesis.github.io/tancredi/problems#forbidden',
                    'title' => 'Access to resource is forbidden with current client privileges'
                );
                $response = $response->withJson($results, 403);
                $response = $response->withHeader('Content-Type', 'application/problem+json');
                $response = $response->withHeader('Content-Language', 'en');
            } else {
                $response = $next($request, $response);
            }
        } else {
            $results = array(
                'type' => 'https://nethesis.github.io/tancredi/problems#forbidden',
                'title' => 'Forbidden',
                'Secretkey' => $request->getHeaderLine('Secretkey'),
                'secret' => $request->getHeaderLine($this->config['secret'])
            );
            $response = $response->withJson($results, 403);
            $response = $response->withHeader('Content-Type', 'application/problem+json');
            $response = $response->withHeader('Content-Language', 'en');
        }
        return $response;
    }
}

