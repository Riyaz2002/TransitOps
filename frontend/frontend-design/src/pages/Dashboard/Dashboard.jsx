import { useMemo } from "react";
import "./Dashboard.css";
import vehicles from "../../data/vehicles";
import drivers from "../../data/drivers";
import trips from "../../data/trips";

function Dashboard() {
  const stats = useMemo(() => {
    const activeTrips = trips.filter(
      (trip) => trip.status !== "Completed" && trip.status !== "Cancelled",
    ).length;
    const availableDrivers = drivers.filter(
      (driver) => driver.status === "Available",
    ).length;
    const availableVehicles = vehicles.filter(
      (vehicle) => vehicle.status === "Available",
    ).length;

    return [
      { label: "Active Trips", value: activeTrips, tone: "accent" },
      { label: "Available Drivers", value: availableDrivers, tone: "success" },
      {
        label: "Available Vehicles",
        value: availableVehicles,
        tone: "warning",
      },
    ];
  }, []);

  return (
    <div className="dashboard-page">
      <div className="dashboard-hero">
        <div>
          <p className="dashboard-eyebrow">Operations overview</p>
          <h2>Fleet health at a glance</h2>
          <p className="dashboard-copy">
            Keep track of your fleet activity, active trips, and resource
            availability in one place.
          </p>
        </div>
        <div className="dashboard-pill">Live fleet summary</div>
      </div>

      <div className="dashboard-stats">
        {stats.map((item) => (
          <div key={item.label} className={`dashboard-stat ${item.tone}`}>
            <span>{item.label}</span>
            <strong>{item.value}</strong>
          </div>
        ))}
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>Recent operations</h3>
          <ul>
            <li>3 trips are currently in motion.</li>
            <li>2 drivers are on duty today.</li>
            <li>Vehicle availability remains strong.</li>
          </ul>
        </div>
        <div className="dashboard-card">
          <h3>Quick focus</h3>
          <ul>
            <li>Review dispatched trips before departure.</li>
            <li>Confirm maintenance vehicles are offline.</li>
            <li>Balance driver shifts for evening deliveries.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
