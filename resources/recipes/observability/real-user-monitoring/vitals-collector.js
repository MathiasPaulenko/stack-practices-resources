import { onCLS, onINP, onFCP, onLCP, onTTFB } from 'web-vitals';

export function sendToAnalytics(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    id: metric.id,
    rating: metric.rating,
    delta: metric.delta,
    navigationType: metric.navigationType,
    page: window.location.pathname,
  });

  const queued = navigator.sendBeacon?.('/analytics/vitals', body);
  if (!queued) {
    fetch('/analytics/vitals', { body, method: 'POST', keepalive: true });
  }
}

onCLS(sendToAnalytics);
onINP(sendToAnalytics);
onFCP(sendToAnalytics);
onLCP(sendToAnalytics);
onTTFB(sendToAnalytics);
