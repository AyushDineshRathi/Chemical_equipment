import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

export default function UploadTrendChart({ history }) {
  const dates = history
    .slice()
    .reverse()
    .map((item) =>
      new Date(item.uploaded_at).toLocaleDateString()
    );

  const counts = dates.map((_, i) => i + 1);

  const data = {
    labels: dates,
    datasets: [
      {
        label: "Uploads Over Time",
        data: counts,
        borderColor: "#2563eb",
        tension: 0.4,
      },
    ],
  };

  return <Line data={data} />;
}
