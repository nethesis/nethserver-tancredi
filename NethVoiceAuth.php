<?php namespace Tancredi\Entity;

class NethVoiceAuth
{
    private $secret;
    private $static_token;
    private $dbh;

    public function __construct($config) {
        if (!is_array($config) or !array_key_exists('secret',$config) or !array_key_exists('static_token',$config)) {
            throw new RuntimeException('Wrong or missing configuration');
        }
        $this->secret = $config['secret'];
        $this->static_token = $config['static_token'];
        $this->dbh = new \PDO(
            'mysql:dbname=asterisk;host=localhost',
            'tancredi',
            $config['auth_nethvoice_dbpass']
        );
    }

    public function __invoke($request, $response, $next)
    {
        if ($request->isOptions()) {
            $response = $next($request, $response);
        } elseif ($request->hasHeader('StaticToken') and !empty($this->static_token) and $request->getHeaderLine('StaticToken') === $this->static_token) {
            // Local autentication for NethCTI success
            $response = $next($request, $response);
	} elseif ($request->hasHeader('Secretkey') and !empty($this->secret)) {
            $stmt = $this->dbh->prepare("SELECT * FROM ampusers WHERE sections LIKE '%*%' AND username = ?");
            $stmt->execute(array($request->getHeaderLine('User')));
            $user = $stmt->fetchAll();
            $password_sha1 = $user[0]['password_sha1'];
            $username = $user[0]['username'];

            # check the user is valid and is an admin (sections = *)
            if (!$username) {
                return $response->withJson(['error' => 'Forbidden: invalid user'], 403);
            }
            $hash = sha1($username . $password_sha1 . $this->secret);
            if ($request->getHeaderLine('Secretkey') != $hash) {
                $results = array(
                    'type' => 'https://github.com/nethesis/tancredi/wiki/problems#wrong-password',
                    'title' => 'Wrong password'
                );
                $response = $response->withJson($results, 403);
                $response = $response->withHeader('Content-Type', 'application/problem+json');
                $response = $response->withHeader('Content-Language', 'en');
            } else {
                $response = $next($request, $response);
            }
        } else {
            $results = array(
                'type' => 'https://github.com/nethesis/tancredi/wiki/problems#missing-secret',
                'title' => 'Missing secret key',
                'Secretkey' => $request->getHeaderLine('Secretkey'),
                'secret' => $request->getHeaderLine($this->secret)
            );
            $response = $response->withJson($results, 403);
            $response = $response->withHeader('Content-Type', 'application/problem+json');
            $response = $response->withHeader('Content-Language', 'en');
        }
        return $response;
    }
}

