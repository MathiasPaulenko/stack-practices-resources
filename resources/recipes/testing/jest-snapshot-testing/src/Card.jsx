export default function Card({ title, description, imageUrl, loading = false }) {
  if (loading) {
    return <div className="card card--loading">Loading…</div>;
  }

  return (
    <article className="card">
      {imageUrl && <img className="card__image" src={imageUrl} alt="" />}
      <div className="card__body">
        <h3 className="card__title">{title}</h3>
        <p className="card__description">{description}</p>
      </div>
    </article>
  );
}
