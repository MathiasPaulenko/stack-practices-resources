# Front Controller Pattern — Companion Files

Companion resources for the article
[Front Controller Pattern](https://stackpractices.com/patterns/front-controller-pattern/)
on StackPractices.

## Contents

- `java/FrontControllerServlet.java` — canonical J2EE form: one servlet mapped to `/*` dispatches to `Command` objects that return the view.
- `php/index.php` — the `index.php` bootstrap every PHP framework uses (Symfony, Laravel); pair with a rewrite rule routing all URLs here.
- `node/app.js` — Express as a front controller: middleware for shared preprocessing, routes as commands.

## Run

```bash
# PHP (built-in server — every request hits index.php)
php -S localhost:8080 php/index.php

# Node
cd node && npm install express && node app.js
curl -H "Authorization: Bearer valid" http://localhost:3000/user
```

For Java, drop `FrontControllerServlet.java` into any Jakarta/Servlet project with views under `WEB-INF/views/`.

## License

Free to use and adapt under MIT. Attribution appreciated, not required.
