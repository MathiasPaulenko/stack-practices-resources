// Stands in for a third-party charting component you do not control:
// its output carries runtime noise (random sizing), so a snapshot that
// included it would flake on every run.
export default function Chart({ series }) {
  const width = Math.floor(Math.random() * 400);

  return (
    <canvas className="chart" data-series={JSON.stringify(series)} style={{ width }} />
  );
}
