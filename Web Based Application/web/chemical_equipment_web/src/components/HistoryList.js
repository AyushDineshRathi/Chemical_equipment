import React, { useEffect, useState } from "react";
import { getHistory } from "../services/api";

function HistoryList() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await getHistory();
        setHistory(res.data);
      } catch (err) {
        console.error("Failed to fetch history", err);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  if (loading) return <p>Loading history...</p>;

  return (
    <div>
      <h3>Upload History (Last 5)</h3>
      {history.length === 0 ? (
        <p>No uploads yet</p>
      ) : (
        <ul>
          {history.map((item) => (
            <li key={item.id}>
              <strong>{item.file_name}</strong> <br />
              <small>{new Date(item.uploaded_at).toLocaleString()}</small>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default HistoryList;
