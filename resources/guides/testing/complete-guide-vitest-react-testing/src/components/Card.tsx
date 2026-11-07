interface CardProps {
  title: string;
  description?: string;
  image?: string;
}

export function Card({ title, description, image }: CardProps) {
  return (
    <div className="card">
      <h3>{title}</h3>
      {image && <img src={image} alt={title} />}
      {description && <p>{description}</p>}
    </div>
  );
}
