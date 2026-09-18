// SearchBox.jsx — a React island: the only component on the page
// that ships React to the browser.
import { useState, useEffect } from 'react';

export default function SearchBox() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (query.length < 2) {
      setResults([]);
      return;
    }
    const timer = setTimeout(async () => {
      const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
      setResults(await res.json());
    }, 200);
    return () => clearTimeout(timer);
  }, [query]);

  return (
    <div className="search-box">
      <input
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search products..."
      />
      {results.length > 0 && (
        <ul>
          {results.map(r => (
            <li key={r.id}>
              <a href={r.url}>{r.title}</a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
