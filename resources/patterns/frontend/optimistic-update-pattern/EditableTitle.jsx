import React, { useState } from 'react';

function EditableTitle({ item }) {
  const [title, setTitle] = useState(item.title);
  const [version, setVersion] = useState(item.version);
  const [conflict, setConflict] = useState(null);

  const handleSave = async () => {
    const previousTitle = title;
    const previousVersion = version;
    setConflict(null);

    try {
      const response = await fetch(`/api/items/${item.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, version }),
      });

      if (response.status === 409) {
        // Conflict — server has a newer version
        const serverItem = await response.json();
        setConflict({
          serverTitle: serverItem.title,
          yourTitle: title,
        });
        // Roll back to the server version
        setTitle(serverItem.title);
        setVersion(serverItem.version);
        return;
      }

      const updated = await response.json();
      setVersion(updated.version);
    } catch (err) {
      setTitle(previousTitle);
      setVersion(previousVersion);
    }
  };

  return (
    <div>
      <input value={title} onChange={(e) => setTitle(e.target.value)} />
      <button onClick={handleSave}>Save</button>
      {conflict && (
        <div className="conflict-warning">
          Another user edited this title to "{conflict.serverTitle}".
          Your change "{conflict.yourTitle}" was reverted.
        </div>
      )}
    </div>
  );
}
