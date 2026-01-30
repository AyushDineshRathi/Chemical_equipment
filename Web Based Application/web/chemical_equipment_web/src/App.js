import "./styles/theme.css";
import Card from "./components/Card";
import UploadCSV from "./components/uploadCSV";
import TypeDistributionChart from "./components/TypeDistributionChart";
import HistoryList from "./components/HistoryList";
import { useState } from "react";
import Login from "./components/login";
import KPI from "./components/KPI";
import UploadTrendChart from "./components/UploadTrendChart";

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
          
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
              gap: "16px",
              marginBottom: "32px",
            }}
          >
            <KPI label="Total Equipment" value={data.summary.total_equipment} />
            <KPI label="Avg Flow Rate" value={data.summary.average_flowrate.toFixed(1)} unit="L/min" />
            <KPI label="Avg Pressure" value={data.summary.average_pressure.toFixed(2)} unit="bar" />
            <KPI label="Avg Temperature" value={data.summary.average_temperature.toFixed(1)} unit="°C" />
          </div>
          
          {history.length > 1 && (
            <Card title="Upload Trend">
              <UploadTrendChart history={history} />
            </Card>
          )}

          <Card title="Equipment Distribution">
            <TypeDistributionChart
              distribution={data.summary.type_distribution}
            />
          </Card>
        </>
      )}

      <HistoryList onLoad={setHistory} />
    </div>
  );
}

export default App;