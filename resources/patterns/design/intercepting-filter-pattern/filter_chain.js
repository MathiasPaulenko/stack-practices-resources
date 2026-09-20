/**
 * Intercepting Filter pattern — runnable JavaScript example.
 *
 * A filter chain intercepts the request on the way in and the response on
 * the way back. Each filter can preprocess, short-circuit, or postprocess.
 *
 * Run: node filter_chain.js
 */

class HttpRequest {
  constructor(path, headers = {}) {
    this.path = path;
    this.headers = headers;
    this.user = null;
    this.authenticated = false;
  }
}

class HttpResponse {
  constructor() {
    this.status = 200;
    this.headers = {};
    this.body = null;
  }
}

class FilterChain {
  constructor() {
    this.filters = [];
    this.index = 0;
  }

  addFilter(filter) {
    this.filters.push(filter);
    return this;
  }

  doFilter(request, response) {
    if (this.index < this.filters.length) {
      const filter = this.filters[this.index++];
      filter.doFilter(request, response, this);
    }
  }

  // Entry point: reset the cursor so the same chain can serve the next request.
  execute(request, response) {
    this.index = 0;
    this.doFilter(request, response);
  }
}

class AuthenticationFilter {
  doFilter(request, response, chain) {
    const token = request.headers['Authorization'];
    if (token && token.startsWith('Bearer ')) {
      request.user = 'authenticated_user';
      request.authenticated = true;
      chain.doFilter(request, response);
    } else {
      response.status = 401;
      response.body = { error: 'Unauthorized' };
    }
  }
}

class LoggingFilter {
  doFilter(request, response, chain) {
    console.log(`[LOG] -> ${request.path}`);
    chain.doFilter(request, response);
    console.log(`[LOG] <- status ${response.status}`);
  }
}

class CompressionFilter {
  doFilter(request, response, chain) {
    chain.doFilter(request, response);
    const encoding = request.headers['Accept-Encoding'] || '';
    if (encoding.includes('gzip')) {
      response.headers['Content-Encoding'] = 'gzip';
      console.log('[COMPRESS] response compressed');
    }
  }
}

class TargetHandler {
  doFilter(request, response, chain) {
    if (response.status === 200) {
      response.body = { message: `Hello, ${request.user || 'guest'}!` };
    }
  }
}

function buildChain() {
  return new FilterChain()
    .addFilter(new AuthenticationFilter())
    .addFilter(new LoggingFilter())
    .addFilter(new CompressionFilter())
    .addFilter(new TargetHandler());
}

module.exports = {
  HttpRequest,
  HttpResponse,
  FilterChain,
  AuthenticationFilter,
  LoggingFilter,
  CompressionFilter,
  TargetHandler,
  buildChain,
};

if (require.main === module) {
  const chain = buildChain();

  const ok = new HttpRequest('/api/hello', {
    Authorization: 'Bearer abc123',
    'Accept-Encoding': 'gzip',
  });
  const denied = new HttpRequest('/api/hello', {});

  for (const req of [ok, denied]) {
    const res = new HttpResponse();
    chain.execute(req, res);
    console.log(`${req.path} auth=${req.authenticated} -> ${res.status} ${JSON.stringify(res.body)}\n`);
  }
}
