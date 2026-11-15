import Chart from './lib/Chart';

export default function Dashboard({ series }) {
  return (
    <section className="dashboard">
      <h2 className="dashboard__title">Sales</h2>
      <Chart series={series} />
    </section>
  );
}
