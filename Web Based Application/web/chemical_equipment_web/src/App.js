import React, { useState } from "react";
import UploadCSV from "./components/uploadCSV";
import TypeDistributionChart from "./components/TypeDistributionChart";
import HistoryList from "./components/HistoryList";

function App() {
  const [data, setData] = useState(null);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Chemical Equipment Parameter Visualizer</h1>

      <UploadCSV onUploadSuccess={setData} />

      {data && (
          <div>
          <h3>Summary</h3>
          <pre>{JSON.stringify(data.summary, null, 2)}</pre>

          <h3>Equipment Type Distribution</h3>
          <TypeDistributionChart
            distribution={data.summary.type_distribution}
          />
          <hr />
          <HistoryList />
          </div>
      )}
    </div>
  );
}

export default App;