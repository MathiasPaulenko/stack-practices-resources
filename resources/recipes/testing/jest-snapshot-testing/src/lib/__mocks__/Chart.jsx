// Manual mock for src/lib/Chart.jsx — Jest picks this up
// automatically when a test calls jest.mock('./lib/Chart').
export default function Chart() {
  return <div data-testid="chart-stub" />;
}
