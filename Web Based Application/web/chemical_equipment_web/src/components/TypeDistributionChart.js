import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

function TypeDistributionChart({ distribution }) {
  const data = {
    labels: Object.keys(distribution),
    datasets: [
      {
        label: "Equipment Types",
        data: Object.values(distribution),
        backgroundColor: [
          "#4CAF50",
          "#2196F3",
          "#FFC107",
          "#FF5722",
          "#9C27B0",
          "#00BCD4",
        ],
      },
    ],
  };

  return <Pie data={data} />;
}

export default TypeDistributionChart;
