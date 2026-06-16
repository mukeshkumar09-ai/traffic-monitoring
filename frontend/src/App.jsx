import { useEffect, useState } from "react";
import API from "./api";
import TrafficChart from "./components/TrafficChart";

function App() {
  const [count, setCount] = useState(0);
  const [status, setStatus] = useState("");
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const latest = await API.get("/latest");
      console.log("LATEST:", latest.data);

      const trafficStatus = await API.get("/status");
      console.log("STATUS:", trafficStatus.data);

      const historyData = await API.get("/history");
      console.log("HISTORY:", historyData.data);

      setCount(latest.data.vehicle_count);
      setStatus(trafficStatus.data.traffic_status);
      setHistory(historyData.data);
    } catch (error) {
      console.log("ERROR:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>🚦 Smart Traffic Monitoring Dashboard</h1>

      {/* Dashboard Cards */}
      <div
        style={{
          display: "flex",
          gap: "40px",
          marginBottom: "30px",
          marginTop: "20px",
        }}
      >
        <div
          style={{
            border: "1px solid #ccc",
            padding: "20px",
            borderRadius: "10px",
            minWidth: "200px",
          }}
        >
          <h3>Vehicle Count</h3>
          <h1>{count}</h1>
        </div>

        <div
          style={{
            border: "1px solid #ccc",
            padding: "20px",
            borderRadius: "10px",
            minWidth: "200px",
          }}
        >
          <h3>Traffic Status</h3>
          <h1>{status}</h1>
        </div>
      </div>

      {/* Analytics Chart */}
      <h2>📊 Traffic Analytics</h2>

      <TrafficChart history={history} />

      {/* History Section */}
      <h2 style={{ marginTop: "40px" }}>📜 Traffic History</h2>

      <ul>
        {history.map((item) => (
          <li key={item.id}>
            Vehicle Count: {item.vehicle_count}
            {" | "}
            {item.timestamp}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;