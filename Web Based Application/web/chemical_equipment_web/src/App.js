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
    <div style={{ maxWidth: "1100px", margin: "0 auto", padding: "32px" }}>
      <h1 style={{ marginBottom: "8px" }}>
        Chemical Equipment Visualizer
      </h1>
      <p style={{ color: "var(--secondary)", marginBottom: "32px" }}>
        Upload datasets, analyze equipment metrics, and visualize insights.
      </p>

      <UploadCSV onUploadSuccess={setData} />

      {data && (
        <>
          <Card title="Summary">
            <pre style={{ margin: 0 }}>
              {JSON.stringify(data.summary, null, 2)}
            </pre>
          </Card>
          
          {/* KPIs - use safe fallbacks in case API uses alternate key names */}
          {(() => {
            const s = data.summary || {};
            const totalEquipment = s.total_equipment ?? s.total_equipments ?? s.total ?? "-";
            const avgFlow = s.average_flowrate ?? s.averageFlowrate ?? s.avg_flowrate ?? null;
            const avgPressure = s.average_pressure ?? s.averagePressure ?? s.avg_pressure ?? null;
            const avgTemp = s.average_temperature ?? s.averageTemperature ?? s.avg_temperature ?? null;

            return (
              <>
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
                    gap: "16px",
                    marginBottom: "24px",
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "16px" }}>
                    <button
                      onClick={async () => {
                        try {
                          const response = await import("./services/api").then(m => m.generateReport(data.dataset_id));
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
                        padding: "10px 16px",
                        background: "var(--success)",
                        color: "#fff",
                        border: "none",
                        borderRadius: "8px",
                        cursor: "pointer",
                        fontWeight: "600",
                        display: "flex",
                        alignItems: "center",
                        gap: "8px"
                      }}
                    >
                      📄 Download PDF Report
                    </button>
                  </div>

                  <KPI label="Total Equipment" value={totalEquipment} />
                  <KPI label="Avg Flow Rate" value={avgFlow != null ? Number(avgFlow).toFixed(1) : "-"} unit="L/min" />
                  <KPI label="Avg Pressure" value={avgPressure != null ? Number(avgPressure).toFixed(2) : "-"} unit="bar" />
                  <KPI label="Avg Temperature" value={avgTemp != null ? Number(avgTemp).toFixed(1) : "-"} unit="°C" />
                </div>

                <Card title="Parameter Averages">
                  <ParameterAveragesChart averages={s} />
                </Card>

                {history.length > 1 && (
                  <Card title="Upload Trend">
                    <UploadTrendChart history={history} />
                  </Card>
                )}

                <Card title="Equipment Distribution">
                  <TypeDistributionChart
                    distribution={s.type_distribution ?? s.equipment_type_distribution ?? s.typeDistribution}
                  />
                </Card>
              </>
            );
          })()}
        </>
      )}

      <HistoryList onLoad={setHistory} />
    </div>
  );
}

export default App;