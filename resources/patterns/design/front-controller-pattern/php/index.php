<?php
// index.php — every request lands here.
// Apache: RewriteRule ^ index.php [PT,L]  ·  Nginx: try_files $uri /index.php?$args

declare(strict_types=1);

interface Controller {
    public function handle(): string;
}

class HomeController implements Controller {
    public function handle(): string {
        return 'Welcome to the home page';
    }
}

class UserController implements Controller {
    public function handle(): string {
        return 'User profile page';
    }
}

$routes = [
    '/'     => HomeController::class,
    '/user' => UserController::class,
];

$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

// Shared preprocessing: auth check before any controller runs
if (($_SERVER['HTTP_AUTHORIZATION'] ?? '') !== 'Bearer valid') {
    http_response_code(401);
    exit('Unauthorized');
}

$controllerClass = $routes[$path] ?? null;
if ($controllerClass === null) {
    http_response_code(404);
    exit('Not Found');
}

echo (new $controllerClass())->handle();
