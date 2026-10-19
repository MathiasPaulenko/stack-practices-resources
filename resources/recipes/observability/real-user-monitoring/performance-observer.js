import { sendToAnalytics } from './vitals-collector.js';

const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.entryType === 'resource' && entry.duration > 1000) {
      sendToAnalytics({
        name: 'slow-resource',
        value: entry.duration,
        id: entry.name,
        rating: 'poor',
      });
    }
    if (entry.entryType === 'longtask') {
      sendToAnalytics({
        name: 'longtask',
        value: entry.duration,
        id: `longtask-${entry.startTime.toFixed(0)}`,
        rating: entry.duration > 200 ? 'poor' : 'needs-improvement',
      });
    }
  }
});

observer.observe({ entryTypes: ['resource', 'longtask'] });
