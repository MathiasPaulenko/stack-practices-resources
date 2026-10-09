// Real-ish MVC: the model notifies subscribers so the view re-renders
// without the controller polling. TypeScript strict clean.

interface Metric {
  name: string;
  value: number;
}

// Model: data + subscription, no idea who renders it
class DashboardModel {
  private metrics: Metric[] = [];
  private subscribers: (() => void)[] = [];

  addMetric(metric: Metric) {
    this.metrics.push(metric);
    this.notify();
  }

  getMetrics(): Metric[] {
    return [...this.metrics];
  }

  subscribe(cb: () => void) {
    this.subscribers.push(cb);
  }

  private notify() {
    this.subscribers.forEach((cb) => cb());
  }
}

// View: renders whatever the model hands over
class DashboardView {
  constructor(private container: HTMLElement) {}

  render(metrics: Metric[]) {
    this.container.innerHTML = metrics
      .map((m) => `<div class="metric-card"><h3>${m.name}</h3><span class="value">${m.value}</span></div>`)
      .join("");
  }
}

// Controller: fetches into the model; the subscription re-renders
class DashboardController {
  constructor(private model: DashboardModel, private view: DashboardView) {
    this.model.subscribe(() => this.view.render(this.model.getMetrics()));
  }

  async loadMetrics() {
    const data: Metric[] = await fetch("/api/metrics").then((r) => r.json());
    data.forEach((m) => this.model.addMetric(m));
  }
}
