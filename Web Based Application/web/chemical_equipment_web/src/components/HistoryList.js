import React, { useEffect, useState } from "react";
import { getHistory } from "../services/api";
import Card from "./Card";

function HistoryList({ onLoad }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await getHistory();
        setHistory(res.data);
        onLoad(res.data);
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
    <Card title="Upload History">
        <ul style={{ listStyle: "none", padding: 0 }}>
            {history.map((item) => (
            <li
                key={item.id}
                style={{
                padding: "12px",
                borderBottom: "1px solid var(--border)"
                }}
            >
                <strong>{item.file_name}</strong>
                <br />
                <small style={{ color: "var(--secondary)" }}>
                {new Date(item.uploaded_at).toLocaleString()}
                </small>
            </li>
            ))}
        </ul>
    </Card>
  );
}

export default HistoryList;