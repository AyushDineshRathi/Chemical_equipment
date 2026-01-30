import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function ParameterAveragesChart({ averages }) {
  const flow =
    averages?.average_flowrate ?? averages?.averageFlowrate ?? averages?.avg_flowrate ?? null;
  const pressure =
    averages?.average_pressure ?? averages?.averagePressure ?? averages?.avg_pressure ?? null;
  const temperature =
    averages?.average_temperature ?? averages?.averageTemperature ?? averages?.avg_temperature ?? null;

  const hasAny = flow != null || pressure != null || temperature != null;

  if (!hasAny) {
    return (
      <div style={{ padding: "20px", color: "var(--secondary)" }}>
        No parameter averages available.
      </div>
    );
  }

  const labels = ["Flow Rate (L/min)", "Pressure (bar)", "Temperature (°C)"];
  const dataValues = [flow ?? 0, pressure ?? 0, temperature ?? 0];

  const data = {
    labels,
    datasets: [
      {
        label: "Average",
        data: dataValues,
        backgroundColor: ["#4CAF50", "#2196F3", "#FFC107"],
        borderRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      title: {
        display: true,
        text: "Average Equipment Parameters",
        font: { size: 16 },
      },
      tooltip: {
        enabled: true,
        callbacks: {
          label: function (context) {
            const label = context.dataset.label || "";
            const value = context.formattedValue;
            return `${label}: ${value}`;
          },
        },
      },
    },
    scales: {
      x: {
        title: { display: false },
      },
      y: {
        beginAtZero: true,
        title: { display: true, text: "Value" },
      },
    },
  };

  return (
    <div style={{ height: "320px" }}>
      <Bar data={data} options={options} />
    </div>
  );
}
