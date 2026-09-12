# terraform/grafana.tf
resource "grafana_dashboard" "api" {
  config_json = jsonencode({
    title = "API Overview"
    panels = [
      {
        title = "Request Rate"
        type  = "timeseries"
        targets = [{
          expr = "sum(rate(http_requests_total[5m]))"
        }]
      }
    ]
  })
}
