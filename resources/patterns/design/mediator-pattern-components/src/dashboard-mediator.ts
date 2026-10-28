// mediator/DashboardMediator.ts
interface Mediator {
  notify(sender: Component, event: string, data?: unknown): void;
}

abstract class Component {
  constructor(protected mediator: Mediator) {}

  send(event: string, data?: unknown): void {
    this.mediator.notify(this, event, data);
  }
}

class FilterPanel extends Component {
  private selectedRegion = 'all';

  selectRegion(region: string): void {
    this.selectedRegion = region;
    this.send('region-changed', region);
  }
}

class ChartWidget extends Component {
  private data: unknown[] = [];

  updateData(data: unknown[]): void {
    this.data = data;
    this.render();
  }

  private render(): void {
    console.log('Chart rendered with', this.data.length, 'points');
  }
}

class TableWidget extends Component {
  private rows: unknown[] = [];

  updateRows(rows: unknown[]): void {
    this.rows = rows;
    console.log('Table updated with', rows.length, 'rows');
  }
}

class MapWidget extends Component {
  private center = { lat: 0, lng: 0 };

  panTo(center: { lat: number; lng: number }): void {
    this.center = center;
    console.log('Map centered at', center);
  }
}

// Mediator orchestrates all communication
class DashboardMediator implements Mediator {
  private filters: FilterPanel;
  private chart: ChartWidget;
  private table: TableWidget;
  private map: MapWidget;

  setComponents(
    filters: FilterPanel,
    chart: ChartWidget,
    table: TableWidget,
    map: MapWidget
  ): void {
    this.filters = filters;
    this.chart = chart;
    this.table = table;
    this.map = map;
  }

  notify(sender: Component, event: string, data?: unknown): void {
    switch (event) {
      case 'region-changed': {
        const filteredData = this.fetchDataForRegion(data as string);
        this.chart.updateData(filteredData);
        this.table.updateRows(filteredData);
        this.map.panTo(this.getRegionCenter(data as string));
        break;
      }
      case 'chart-point-clicked': {
        const point = data as { lat: number; lng: number };
        this.map.panTo(point);
        break;
      }
    }
  }

  private fetchDataForRegion(region: string): unknown[] {
    return [{ id: 1, region }];
  }

  private getRegionCenter(region: string): { lat: number; lng: number } {
    const centers: Record<string, { lat: number; lng: number }> = {
      'north': { lat: 45, lng: 0 },
      'south': { lat: -45, lng: 0 },
    };
    return centers[region] || { lat: 0, lng: 0 };
  }
}

// Usage
const mediator = new DashboardMediator();
const filters = new FilterPanel(mediator);
const chart = new ChartWidget(mediator);
const table = new TableWidget(mediator);
const map = new MapWidget(mediator);

mediator.setComponents(filters, chart, table, map);
filters.selectRegion('north');
