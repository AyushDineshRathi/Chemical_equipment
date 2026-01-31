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
      if (error.response && error.response.status === 401) {
          alert("Session expired. Please login again.");
      } else {
          alert("Upload failed. Please check your file and connection.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Upload Dataset">
      <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
        
        <label 
          htmlFor="file-upload" 
          style={{
            border: "2px dashed var(--border)",
            borderRadius: "8px",
            padding: "32px",
            textAlign: "center",
            cursor: "pointer",
            transition: "border-color 0.2s, background 0.2s",
            background: file ? "#f0f9ff" : "transparent",
            borderColor: file ? "var(--primary)" : "var(--border)"
          }}
          onDragOver={(e) => { e.preventDefault(); e.currentTarget.style.borderColor = "var(--primary)"; }}
          onDragLeave={(e) => { e.currentTarget.style.borderColor = "var(--border)"; }}
          onDrop={(e) => { 
            e.preventDefault(); 
            e.currentTarget.style.borderColor = "var(--primary)";
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
              setFile(e.dataTransfer.files[0]);
            }
          }}
        >
          <input
            id="file-upload"
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
            style={{ display: "none" }}
          />
          <div style={{ fontSize: "24px", marginBottom: "8px" }}>📂</div>
          <p style={{ margin: 0, fontWeight: "500", color: "var(--text)" }}>
             {file ? file.name : "Click to select or drag CSV file"}
          </p>
          {!file && <p style={{ margin: "4px 0 0 0", fontSize: "12px", color: "var(--text-light)" }}>Supported format: .csv</p>}
        </label>

        <button
          onClick={handleUpload}
          disabled={loading || !file}
          style={{
            padding: "12px 16px",
            background: loading || !file ? "var(--secondary)" : "var(--primary)",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            cursor: loading || !file ? "not-allowed" : "pointer",
            fontWeight: "600",
            fontSize: "14px",
            transition: "background 0.2s"
          }}
        >
          {loading ? "Uploading..." : "Upload CSV"}
        </button>
      </div>
    </Card>
  );
}

export default UploadCSV;
