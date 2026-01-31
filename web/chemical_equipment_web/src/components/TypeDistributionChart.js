import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend, Title } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend, Title);

function TypeDistributionChart({ distribution }) {
  // Safety: support multiple possible key names or an explicit object
  const dist = distribution || {};
  const labels = Object.keys(dist);
  const values = Object.values(dist);

  if (labels.length === 0) {
    return (
      <div style={{ padding: "20px", color: "var(--secondary)" }}>
        No equipment type distribution data available.
      </div>
    );
  }

  const palette = ["#4CAF50", "#2196F3", "#FFC107", "#FF5722", "#9C27B0", "#00BCD4", "#795548", "#607D8B"];

  const data = {
    labels,
    datasets: [
      {
        label: "Equipment Types",
        data: values,
        backgroundColor: labels.map((_, i) => palette[i % palette.length]),
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: "bottom" },
      title: { display: true, text: "Equipment Type Distribution" },
      tooltip: { enabled: true },
    },
  };

  return (
    <div style={{ height: "320px" }}>
      <Pie data={data} options={options} />
    </div>
  );
}

export default TypeDistributionChart;
