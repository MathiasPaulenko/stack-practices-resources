# Contributing to StackPractices Resources

This repository hosts code recipes, design patterns, technical guides and documentation templates referenced from [stackpractices.com](https://stackpractices.com).

## How to add a resource

1. Pick the right place under `resources/`:

   ```text
   resources/{type}/{topic}/{slug}/
   ```

   - `type` must be one of: `recipes`, `patterns`, `guides`, `docs`.
   - `topic` should match a topic slug already used on stackpractices.com (e.g. `api`, `authentication`, `databases`, `devops`, `security`, `performance`, `testing`, `architecture`, `caching`, `concurrency`, `frontend`, `graphql`, `infrastructure`, `messaging`, `observability`, `serverless`, `ai`, `data`, `design`, `file-handling`).
   - `slug` is a short, unique, kebab-case identifier.

2. Create a `meta.json` file in that folder. Example:

   ```json
   {
     "title": "Redis LRU Cache with Python",
     "title_es": "Cache LRU con Redis y Python",
     "description": "Complete runnable example of an LRU cache backed by Redis with async support.",
     "description_es": "Ejemplo completo y ejecutable de cache LRU con Redis y soporte async.",
     "type": "recipes",
     "topic": "caching",
     "slug": "redis-lru-cache",
     "source_urls": [
       "https://stackpractices.com/recipes/redis-lru-cache/"
     ],
     "language": "python",
     "tags": ["redis", "caching", "python", "async"],
     "files": [
       "main.py",
       "requirements.txt"
     ]
   }
   ```

3. Add the actual files. If you do not list them in `files`, the build script will discover them automatically, but explicit lists are safer.

4. Optional: add `README.md` and `README.es.md` with usage instructions.

5. Run the catalog builder locally:

   ```bash
   npm install
   npm run build
   ```

   This generates `resources.json` used by the GitHub Pages browser.

6. Commit and push. The GitHub Action will rebuild and redeploy the browser.

## Reusable assets

If a snippet or helper is reused by multiple resources, place it under `shared/`:

```text
shared/snippets/python/caching/redis_helper.py
```

Reference it from the resource `README.md` or `meta.json` `shared_dependencies` field.

## Validation

The build script checks that:

- `meta.json` contains `title`, `description`, `type`, `topic`, `slug`.
- Every file listed in `files` exists.
- `source_urls` are valid URLs.

If the build fails, the GitHub Pages deploy does not run.
