sub vcl_recv {
  # Tag hashed static assets so vcl_fetch can treat them as immutable
  if (req.url.ext ~ "^(css|js|png|jpg|woff2)$") {
    set req.http.X-Static = "true";
  }
}

sub vcl_fetch {
  if (req.http.X-Static == "true") {
    set beresp.ttl = 365d;
    set beresp.http.Cache-Control = "public, max-age=31536000, immutable";
    set beresp.http.Surrogate-Key = "static";
  }
}
