import "./styles/theme.css";
import Card from "./components/Card";
import UploadCSV from "./components/uploadCSV";
import TypeDistributionChart from "./components/TypeDistributionChart";
import HistoryList from "./components/HistoryList";
import { useState } from "react";
import Login from "./components/login";
import KPI from "./components/KPI";
import UploadTrendChart from "./components/UploadTrendChart";
import ParameterAveragesChart from "./components/ParameterAveragesChart";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);

  if (!token) {
    return <Login onLogin={setToken} />;
  }

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      {/* Navbar */}
      <header style={{
        background: "#ffffff",
        borderBottom: "1px solid var(--border)",
        padding: "16px 32px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        boxShadow: "var(--shadow-sm)"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div style={{ 
            width: "32px", height: "32px", 
            background: "var(--primary)", 
            borderRadius: "8px" 
          }}></div>
          <h1 style={{ fontSize: "20px", color: "var(--text)" }}>Chemical Equipment Visualizer</h1>
        </div>
        <button 
          onClick={() => {
            setToken(null);
            localStorage.removeItem("token");
          }}
          style={{
            background: "transparent",
            border: "1px solid var(--border)",
            padding: "8px 16px",
            borderRadius: "6px",
            fontSize: "14px",
            cursor: "pointer",
            color: "var(--text-light)"
          }}
        >
          Logout
        </button>
      </header>

      {/* Main Content */}
      <main style={{ flex: 1, padding: "32px", maxWidth: "1200px", margin: "0 auto", width: "100%" }}>
        
        {/* Intro / Upload Section */}
        <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: "24px", marginBottom: "32px" }}>
          <div>
            <h2 style={{ fontSize: "24px", marginBottom: "8px" }}>Dashboard Overview</h2>
             <p style={{ color: "var(--text-light)", marginBottom: "24px" }}>
              Upload your equipment datasets to generate reports and visualize key metrics.
            </p>
            <UploadCSV onUploadSuccess={setData} />
          </div>
          <HistoryList onLoad={setHistory} />
        </div>

        {data && (
          <div className="fade-in" style={{ animation: "fadeIn 0.5s ease-in" }}>
            
            {/* Action Bar */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
               <h3 style={{ fontSize: "20px" }}>Analysis Results: ID #{data.dataset_id}</h3>
               <button
                  onClick={async () => {
                    try {
                      // Import dynamically or use standard import if hoisted, keeping dynamic for safety as in original
                      const api = await import("./services/api");
                      const response = await api.generateReport(data.dataset_id);
                      const url = window.URL.createObjectURL(new Blob([response.data]));
                      const link = document.createElement("a");
                      link.href = url;
                      link.setAttribute("download", `equipment_report_${data.dataset_id}.pdf`);
                      document.body.appendChild(link);
                      link.click();
                      link.remove();
                    } catch (err) {
                      console.error("Download failed", err);
                      alert("Failed to download report");
                    }
                  }}
                  style={{
                    padding: "10px 20px",
                    background: "var(--success)",
                    color: "#fff",
                    border: "none",
                    borderRadius: "8px",
                    cursor: "pointer",
                    fontWeight: "600",
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                    boxShadow: "var(--shadow-sm)",
                    transition: "background 0.2s"
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = "var(--success-hover)"}
                  onMouseLeave={(e) => e.currentTarget.style.background = "var(--success)"}
                >
                  <span style={{ fontSize: "18px" }}>📄</span> Download Report
                </button>
            </div>

            {/* KPIs Grid */}
            {(() => {
              const s = data.summary || {};
              const totalEquipment = s.total_equipment ?? s.total_equipments ?? s.total ?? "-";
              const avgFlow = s.average_flowrate ?? s.averageFlowrate ?? s.avg_flowrate ?? null;
              const avgPressure = s.average_pressure ?? s.averagePressure ?? s.avg_pressure ?? null;
              const avgTemp = s.average_temperature ?? s.averageTemperature ?? s.avg_temperature ?? null;

              return (
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
                    gap: "24px",
                    marginBottom: "32px",
                  }}
                >
                  <KPI label="Total Equipment" value={totalEquipment} unit="Units" />
                  <KPI label="Avg Flow Rate" value={avgFlow != null ? Number(avgFlow).toFixed(1) : "-"} unit="L/min" />
                  <KPI label="Avg Pressure" value={avgPressure != null ? Number(avgPressure).toFixed(2) : "-"} unit="bar" />
                  <KPI label="Avg Temperature" value={avgTemp != null ? Number(avgTemp).toFixed(1) : "-"} unit="°C" />
                </div>
              );
            })()}

            {/* Charts Grid */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(400px, 1fr))", gap: "24px" }}>
               {/* Summary JSON Dump (Optional, maybe hidden or collapsed) */}
               {/* Keeping it simple as requested, moving charts up */}
               
               <Card title="Parameter Averages" style={{ height: "100%" }}>
                  <ParameterAveragesChart averages={data.summary || {}} />
               </Card>

               <Card title="Equipment Distribution" style={{ height: "100%" }}>
                  <TypeDistributionChart
                    distribution={data.summary?.type_distribution ?? {}}
                  />
               </Card>

               {history.length > 1 && (
                 <Card title="Upload Trend" style={{ gridColumn: "1 / -1" }}>
                    <UploadTrendChart history={history} />
                 </Card>
               )}
            </div>

          </div>
        )}
      </main>
    </div>
  );
}

export default App;