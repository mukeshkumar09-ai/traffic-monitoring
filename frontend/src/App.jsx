import { useEffect, useState } from "react";
import API from "./api";
import TrafficChart from "./components/TrafficChart";

import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";

function App() {

  const [count, setCount] = useState(0);
  const [status, setStatus] = useState("");
  const [history, setHistory] = useState([]);

  const [peakTraffic, setPeakTraffic] = useState(0);
  const [averageTraffic, setAverageTraffic] = useState(0);
  const [totalRecords, setTotalRecords] = useState(0);

  const [lastUpdated, setLastUpdated] = useState("");

  useEffect(() => {

    fetchData();

    const interval = setInterval(() => {
      fetchData();
    }, 5000);

    return () => clearInterval(interval);

  }, []);

  const fetchData = async () => {

    try {

      const latest = await API.get("/latest");
      const trafficStatus = await API.get("/status");
      const historyData = await API.get("/history");
      const analytics = await API.get("/analytics");

      setCount(latest.data.vehicle_count);

      setStatus(
        trafficStatus.data.traffic_status
      );

      setHistory(historyData.data);

      setPeakTraffic(
        analytics.data.peak_traffic
      );

      setAverageTraffic(
        analytics.data.average_traffic
      );

      setTotalRecords(
        analytics.data.total_records
      );

      setLastUpdated(
        new Date().toLocaleTimeString()
      );

    } catch (error) {

      console.log("Error:", error);

    }
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">
            🚦 Smart Traffic Monitoring System
          </Typography>
        </Toolbar>
      </AppBar>

      <Container sx={{ mt: 2 }}>

        <Typography
          variant="body2"
          sx={{
            textAlign: "right",
            mb: 2,
            color: "gray",
          }}
        >
          Last Updated: {lastUpdated}
        </Typography>

        {/* Top Cards */}

        <Grid container spacing={3}>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6">
                  Vehicle Count
                </Typography>

                <Typography variant="h3">
                  {count}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6">
                  Traffic Status
                </Typography>

                <Typography variant="h4">
                  {status}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6">
                  Active Cameras
                </Typography>

                <Typography variant="h3">
                  1
                </Typography>
              </CardContent>
            </Card>
          </Grid>

        </Grid>

        {/* Analytics Cards */}

        <Grid container spacing={3} sx={{ mt: 1 }}>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6">
                  📈 Peak Traffic
                </Typography>

                <Typography variant="h4">
                  {peakTraffic}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6">
                  📊 Average Traffic
                </Typography>

                <Typography variant="h4">
                  {averageTraffic}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6">
                  📋 Total Records
                </Typography>

                <Typography variant="h4">
                  {totalRecords}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

        </Grid>

        {/* Graph */}

        <Typography
          variant="h5"
          sx={{ mt: 5, mb: 2 }}
        >
          📊 Traffic Analytics
        </Typography>

        <TrafficChart history={history} />

        {/* Smart Alerts */}

        <Typography
          variant="h5"
          sx={{ mt: 5, mb: 2 }}
        >
          🚨 Smart Alerts
        </Typography>

        {count > averageTraffic * 1.5 ? (

          <Card
            sx={{
              backgroundColor: "#ffebee",
              borderLeft: "6px solid red",
              mb: 3,
            }}
          >
            <CardContent>

              <Typography variant="h6">
                🚨 Traffic Spike Detected
              </Typography>

              <Typography>
                Current Count: {count}
              </Typography>

              <Typography>
                Average Traffic: {averageTraffic}
              </Typography>

              <Typography>
                Status: {status}
              </Typography>

            </CardContent>
          </Card>

        ) : (

          <Card
            sx={{
              backgroundColor: "#e8f5e9",
              borderLeft: "6px solid green",
              mb: 3,
            }}
          >
            <CardContent>

              <Typography variant="h6">
                ✅ Traffic Normal
              </Typography>

              <Typography>
                Current Count: {count}
              </Typography>

            </CardContent>
          </Card>

        )}

        {/* History */}

        <Typography
          variant="h5"
          sx={{ mt: 5, mb: 2 }}
        >
          📜 Traffic History
        </Typography>

        <Paper>

          <Table>

            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Vehicle Count</TableCell>
                <TableCell>Timestamp</TableCell>
              </TableRow>
            </TableHead>

            <TableBody>

              {history.map((item) => (

                <TableRow key={item.id}>

                  <TableCell>
                    {item.id}
                  </TableCell>

                  <TableCell>
                    {item.vehicle_count}
                  </TableCell>

                  <TableCell>
                    {item.timestamp}
                  </TableCell>

                </TableRow>

              ))}

            </TableBody>

          </Table>

        </Paper>

      </Container>
    </>
  );
}

export default App;