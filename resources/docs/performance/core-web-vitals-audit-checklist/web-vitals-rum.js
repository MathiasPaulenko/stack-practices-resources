// RUM collection with the web-vitals library.
// npm i web-vitals — then import this from your app entry point.
// Sends LCP, INP and CLS to your analytics endpoint at page hide.

import { onLCP, onINP, onCLS } from 'web-vitals';

const endpoint = '/api/vitals';

function send(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating, // 'good' | 'needs-improvement' | 'poor'
    delta: metric.delta,
    id: metric.id,
    page: location.pathname,
  });
  // sendBeacon survives page unload; fetch keepalive is the fallback
  if (navigator.sendBeacon) {
    navigator.sendBeacon(endpoint, body);
  } else {
    fetch(endpoint, { method: 'POST', body, keepalive: true });
  }
}

// reportAllChanges buffers and flushes on visibility change
onLCP(send, { reportAllChanges: true });
onINP(send, { reportAllChanges: true });
onCLS(send, { reportAllChanges: true });

// Attribution builds (web-vitals/attribution) also report which element
// caused the metric — useful for LCP element and CLS source discovery.
