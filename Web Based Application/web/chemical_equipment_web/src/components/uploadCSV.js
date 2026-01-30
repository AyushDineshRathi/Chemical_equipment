import React, { useState } from "react";
import { uploadCSV } from "../services/api";
import Card from "./Card";

function UploadCSV({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    setLoading(true);

    try {
      const response = await uploadCSV(file);
      console.log("Upload response:", response.data);

      if (onUploadSuccess) {
        onUploadSuccess(response.data);
      }
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Upload Dataset">
        <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
        style={{ marginBottom: "12px" }}
        />

        <br />

        <button
        onClick={handleUpload}
        disabled={loading}
        style={{
            padding: "10px 16px",
            background: "var(--primary)",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer"
        }}
        >
        {loading ? "Uploading..." : "Upload CSV"}
        </button>
    </Card>
    );
}

export default UploadCSV;
