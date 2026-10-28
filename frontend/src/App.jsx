import { useEffect, useState } from "react";
import "./App.css";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine,
} from "recharts";

const API = "http://127.0.0.1:8000";

function App() {
  const [status, setStatus] = useState("Checking...");
  const [metrics, setMetrics] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [error, setError] = useState("");


  useEffect(() => {
    fetch(`${API}/health`)
      .then((response) => {
        if (!response.ok) throw new Error("Backend unavailable");
        return response.json();
      })
      .then(() => setStatus("Connected"))
      .catch(() => setStatus("Offline"));

    fetch(`${API}/api/chart-data`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Chart data unavailable");
        }
        return response.json();
      })
      .then((data) => setChartData(data.data ?? []))
      .catch((err) => console.error("Chart data error:", err));
  }, []);

  useEffect(() => {
    fetch(`${API}/api/metrics`)
      .then((response) => {
        if (!response.ok) throw new Error("Failed to load metrics");
        return response.json();
      })
      .then((data) => {
        if (data.error) throw new Error(data.error);
        setMetrics(data);
      })
      .catch(() => setError("Unable to load metrics"));
  }, []);

  return (
    <main className="dashboard">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">W</div>
          <div>
            <h1>VaayuDev</h1>
            <p>Renewable Energy Intelligence</p>
          </div>
        </div>
        <span className={`connection ${status === "Connected" ? "online" : ""}`}>
          <span className="dot" />
          API {status}
        </span>
      </header>

      <section className="intro">
        <p className="eyebrow">UK NATIONAL WIND GENERATION</p>
        <h2>Day-ahead forecast intelligence</h2>
        <p>
          Compare wind generation forecasts against actual output to support
          better electricity procurement decisions.
        </p>
        <div className="period">ANALYSIS PERIOD <strong>01–31 JAN 2026</strong></div>
      </section>

      <section className="metrics">
        <article className="metric-card">
          <p>Mean Absolute Error</p>
          <h3>{metrics ? metrics.mae.toLocaleString() : "—"}</h3>
          <span>MW · Lower is better</span>
        </article>
        <article className="metric-card">
          <p>Root Mean Square Error</p>
          <h3>{metrics ? metrics.rmse.toFixed(2) : "—"}</h3>
          <span>MW · Penalises larger errors</span>
        </article>
        <article className="metric-card">
          <p>Forecast Bias</p>
          <h3>{metrics ? metrics.bias.toFixed(2) : "—"}</h3>
          <span>MW · Positive means overforecast</span>
        </article>
      </section>


      <section className="panel chart-panel">
        <div>
          <p className="eyebrow">GENERATION ANALYSIS</p>
          <h3>Forecast vs actual generation</h3>
          <p className="muted">
            Hourly wind generation · January 2026 · MW
          </p>
        </div>

        {chartData.length > 0 ? (
          <div style={{ width: "100%", height: 340, marginTop: 24 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={chartData}
                margin={{ top: 8, right: 12, left: 8, bottom: 8 }}
              >
                <CartesianGrid stroke="#293a31" strokeDasharray="3 3" />
                <XAxis
                  dataKey="time"
                  tick={{ fill: "#9aaba0", fontSize: 11 }}
                  interval={71}
                  angle={-25}
                  textAnchor="end"
                  height={65}
                />
                <YAxis
                  tick={{ fill: "#9aaba0", fontSize: 11 }}
                  width={65}
                  label={{
                    value: "Generation (MW)",
                    angle: -90,
                    position: "insideLeft",
                    fill: "#9aaba0",
                  }}
                />
                <Tooltip
                  contentStyle={{
                    background: "#111914",
                    border: "1px solid #34483a",
                    borderRadius: 8,
                    color: "#edf5f0",
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="actual"
                  name="Actual"
                  stroke="#b9f36b"
                  dot={false}
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="forecast"
                  name="Forecast"
                  stroke="#62b7ff"
                  dot={false}
                  strokeWidth={2}
                />
                {/* <Line
                  type="monotone"
                  dataKey="error"
                  name="Forecast Error"
                  stroke="#ff8a65"
                  dot={false}
                  strokeWidth={1.5}
                /> */}
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p className="muted">Loading chart data… Check that the backend is running.</p>
        )}

        <div className="quality-summary">
          <p className="eyebrow">DATA QUALITY</p>
          <p className="muted">
            {metrics
              ? `${metrics.matched_records} matched hourly periods · ${metrics.missing_forecasts} missing forecasts`
              : "Metrics are loading."}
          </p>
        </div>
      </section>
      <section className="panel chart-panel">
  <div>
    <p className="eyebrow">FORECAST PERFORMANCE</p>
    <h3>Forecast error over time</h3>
    <p className="muted">
      Positive = overforecast · Negative = underforecast · MW
    </p>
  </div>

  {chartData.length > 0 && (
    <ResponsiveContainer width="100%" height={250}>
      <LineChart data={chartData}>
        <CartesianGrid stroke="#293a31" strokeDasharray="3 3" />
        <XAxis
          dataKey="time"
          tick={{ fill: "#9aaabe", fontSize: 10 }}
          minTickGap={30}
        />
        <YAxis tick={{ fill: "#9aaabe", fontSize: 11 }} />
        <Tooltip />
        <ReferenceLine y={0} stroke="#9aaabe" />
        <Line
          type="monotone"
          dataKey="error"
          name="Forecast Error"
          stroke="#ff8a65"
          dot={false}
          strokeWidth={1.5}
        />
      </LineChart>
    </ResponsiveContainer>
  )}
</section>


      <footer>
        <span>Data source: Elexon BMRS · FUELHH & WINDFOR</span>
        <span>Wind-only analysis · January 2026</span>
      </footer>
    </main>
  );
}

export default App;
