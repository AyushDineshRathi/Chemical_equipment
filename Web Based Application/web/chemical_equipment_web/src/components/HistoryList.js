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
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
            {history.map((item) => (
            <li
                key={item.id}
                style={{
                  padding: "16px",
                  borderBottom: "1px solid var(--border)",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  transition: "background 0.2s"
                }}
                className="history-item"
                onMouseEnter={(e) => e.currentTarget.style.background = "#f1f5f9"}
                onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}
            >
                <span style={{ fontWeight: "500", color: "var(--text)" }}>{item.file_name}</span>
                <small style={{ 
                  color: "var(--text-light)", 
                  background: "#e2e8f0", 
                  padding: "4px 8px", 
                  borderRadius: "99px",
                  fontSize: "12px"
                }}>
                {new Date(item.uploaded_at).toLocaleDateString()}
                </small>
            </li>
            ))}
        </ul>
    </Card>
  );
}

export default HistoryList;