from prometheus_client import Summary

REQUEST_SIZE = Summary(
    "request_size_bytes",
    "Request payload size in bytes",
    ["endpoint"]
)

if __name__ == "__main__":
    REQUEST_SIZE.labels(endpoint="/upload").observe(1024)
    REQUEST_SIZE.labels(endpoint="/upload").observe(5120)
    REQUEST_SIZE.labels(endpoint="/upload").observe(256)

    print("Summary metric created with 3 observations")
    print("Access quantiles via: REQUEST_SIZE.labels(endpoint='/upload')._quantiles")
