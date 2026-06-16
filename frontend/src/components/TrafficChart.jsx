import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function TrafficChart({ history }) {

  const data = {
    labels: history.map((item) => item.id),

    datasets: [
      {
        label: "Vehicle Count",
        data: history.map(
          (item) => item.vehicle_count
        ),
        borderColor: "rgb(75, 192, 192)",
        backgroundColor: "rgb(75, 192, 192)",
        tension: 0.3,
      },
    ],
  };

  const options = {
    responsive: true,

    plugins: {
      legend: {
        labels: {
          color: "white",
        },
      },
    },

    scales: {
      x: {
        ticks: {
          color: "white",
        },
      },

      y: {
        ticks: {
          color: "white",
        },
      },
    },
  };

  return (
    <div
      style={{
        width: "800px",
        marginTop: "20px",
      }}
    >
      <Line
        data={data}
        options={options}
      />
    </div>
  );
}

export default TrafficChart;