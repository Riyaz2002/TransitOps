import { useEffect, useMemo, useState } from "react";
import "../Vehicle/Vehicle.css";
import tripData from "../../data/trips";
import vehicles from "../../data/vehicles";
import drivers from "../../data/drivers";
import { createTripApi, getTripsApi, updateTripApi } from "../../api/tripApi";

const emptyTrip = {
  trip_number: "",
  source: "",
  destination: "",
  vehicle_id: "",
  driver_id: "",
  cargo_weight: "",
  planned_distance: "",
  actual_distance: "",
  start_odometer: "",
  end_odometer: "",
  fuel_consumed: "",
  status: "Draft",
};

const getVehicleName = (vehicleId) => {
  const numericId = Number(vehicleId);
  const vehicle = vehicles.find((item) => item.id === numericId);
  return vehicle?.name || vehicle?.number || "Unassigned";
};

const getDriverName = (driverId) => {
  const numericId = Number(driverId);
  const driver = drivers.find((item) => item.id === numericId);
  return driver?.name || "Unassigned";
};

function Trip({ dataMode }) {
  const [trips, setTrips] = useState(tripData);
  const [selectedTrip, setSelectedTrip] = useState(null);
  const [formData, setFormData] = useState(emptyTrip);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortKey, setSortKey] = useState("trip_number");

  const isEditing = Boolean(selectedTrip);
  const isApiMode = dataMode === "api";

  useEffect(() => {
    const loadTrips = async () => {
      setError("");
      setShowForm(false);
      setSelectedTrip(null);
      setFormData(emptyTrip);

      if (!isApiMode) {
        setTrips(tripData);
        return;
      }

      setIsLoading(true);
      try {
        const data = await getTripsApi();
        setTrips(Array.isArray(data) ? data : []);
      } catch {
        setError("Unable to load trips from API.");
        setTrips([]);
      } finally {
        setIsLoading(false);
      }
    };

    loadTrips();
  }, [isApiMode]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((currentData) => ({ ...currentData, [name]: value }));
  };

  const handleCreate = () => {
    setSelectedTrip(null);
    setFormData(emptyTrip);
    setShowForm(true);
    setError("");
  };

  const handleSelect = (trip) => {
    setSelectedTrip(trip);
    setFormData(trip);
    setShowForm(true);
    setError("");
  };

  const filteredTrips = useMemo(() => {
    const query = searchTerm.trim().toLowerCase();

    const matches = trips.filter((trip) => {
      if (!query) {
        return true;
      }

      return [trip.trip_number, trip.source, trip.destination, trip.status]
        .join(" ")
        .toLowerCase()
        .includes(query);
    });

    return [...matches].sort((a, b) => {
      if (sortKey === "status") {
        return a.status.localeCompare(b.status);
      }
      if (sortKey === "destination") {
        return a.destination.localeCompare(b.destination);
      }
      return (a.trip_number || "").localeCompare(b.trip_number || "");
    });
  }, [searchTerm, sortKey, trips]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    try {
      const payload = {
        ...formData,
        vehicle_id: formData.vehicle_id ? Number(formData.vehicle_id) : null,
        driver_id: formData.driver_id ? Number(formData.driver_id) : null,
        cargo_weight: Number(formData.cargo_weight || 0),
        planned_distance: Number(formData.planned_distance || 0),
        actual_distance: formData.actual_distance
          ? Number(formData.actual_distance)
          : null,
        start_odometer: Number(formData.start_odometer || 0),
        end_odometer: Number(formData.end_odometer || 0),
        fuel_consumed: formData.fuel_consumed
          ? Number(formData.fuel_consumed)
          : null,
      };

      const savedTrip = isEditing
        ? isApiMode
          ? await updateTripApi(selectedTrip.id, payload)
          : { ...payload, id: selectedTrip.id }
        : isApiMode
          ? await createTripApi(payload)
          : { ...payload, id: Date.now() };

      setTrips((currentTrips) =>
        isEditing
          ? currentTrips.map((trip) =>
              trip.id === savedTrip.id ? savedTrip : trip,
            )
          : [savedTrip, ...currentTrips],
      );
      setSelectedTrip(savedTrip);
      setFormData(savedTrip);
      setShowForm(true);
    } catch {
      setError("Unable to save trip.");
    }
  };

  return (
    <div className="vehicle-page">
      <div className="vehicle-actions">
        <div className="vehicle-toolbar">
          <p>
            {isLoading ? "Loading trips..." : `${filteredTrips.length} trips`}
            <span className="vehicle-mode-label">
              {isApiMode ? "API Mode" : "Dummy Mode"}
            </span>
          </p>
          <div className="vehicle-filter-bar">
            <input
              type="text"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              placeholder="Search trips"
            />
            <select
              value={sortKey}
              onChange={(event) => setSortKey(event.target.value)}
            >
              <option value="trip_number">Sort by trip</option>
              <option value="status">Sort by status</option>
              <option value="destination">Sort by destination</option>
            </select>
          </div>
        </div>
        <button
          type="button"
          className="create-vehicle-btn"
          onClick={handleCreate}
        >
          Add Trip
        </button>
      </div>

      {error && <p className="vehicle-error">{error}</p>}

      <div className="vehicle-manager">
        <div className="vehicle-grid">
          {filteredTrips.map((trip) => (
            <article
              key={trip.id}
              className="vehicle-card"
              onClick={() => handleSelect(trip)}
            >
              <div className="vehicle-card-content">
                <div className="driver-card-header">
                  <div>
                    <h3>{trip.trip_number || `Trip #${trip.id}`}</h3>
                    <p className="driver-role">
                      {trip.source} → {trip.destination}
                    </p>
                  </div>
                  <span
                    className={`driver-status-pill ${trip.status.toLowerCase().replace(/\s+/g, "-")}`}
                  >
                    {trip.status}
                  </span>
                </div>
                <div className="driver-details-list">
                  <div className="driver-detail-item">
                    <span className="driver-detail-label">Vehicle</span>
                    <span>
                      {trip.vehicle_name || getVehicleName(trip.vehicle_id)}
                    </span>
                  </div>
                  <div className="driver-detail-item">
                    <span className="driver-detail-label">Driver</span>
                    <span>
                      {trip.driver_name || getDriverName(trip.driver_id)}
                    </span>
                  </div>
                  <div className="driver-detail-item">
                    <span className="driver-detail-label">Cargo</span>
                    <span>{trip.cargo_weight}</span>
                  </div>
                  <div className="driver-detail-item">
                    <span className="driver-detail-label">Distance</span>
                    <span>{trip.planned_distance}</span>
                  </div>
                </div>
              </div>
            </article>
          ))}
        </div>

        {showForm && (
          <form className="vehicle-form" onSubmit={handleSubmit}>
            <div className="vehicle-form-header">
              <div>
                <h2>{isEditing ? "Edit Trip" : "Create Trip"}</h2>
                <p>
                  {isEditing
                    ? formData.trip_number || `Trip #${formData.id}`
                    : "New record"}
                </p>
              </div>
              <button
                type="button"
                className="close-form-btn"
                onClick={() => setShowForm(false)}
              >
                x
              </button>
            </div>

            <label>
              Trip Number
              <input
                name="trip_number"
                value={formData.trip_number || ""}
                onChange={handleChange}
                placeholder="TRIP-001"
              />
            </label>
            <label>
              Source
              <input
                name="source"
                value={formData.source || ""}
                onChange={handleChange}
                required
              />
            </label>
            <label>
              Destination
              <input
                name="destination"
                value={formData.destination || ""}
                onChange={handleChange}
                required
              />
            </label>
            <label>
              Vehicle
              <select
                name="vehicle_id"
                value={formData.vehicle_id || ""}
                onChange={handleChange}
              >
                <option value="">Select vehicle</option>
                {vehicles.map((vehicle) => (
                  <option key={vehicle.id} value={vehicle.id}>
                    {vehicle.name}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Driver
              <select
                name="driver_id"
                value={formData.driver_id || ""}
                onChange={handleChange}
              >
                <option value="">Select driver</option>
                {drivers.map((driver) => (
                  <option key={driver.id} value={driver.id}>
                    {driver.name}
                  </option>
                ))}
              </select>
            </label>
            <div className="vehicle-form-row">
              <label>
                Cargo Weight
                <input
                  name="cargo_weight"
                  value={formData.cargo_weight || ""}
                  onChange={handleChange}
                />
              </label>
              <label>
                Planned Distance
                <input
                  name="planned_distance"
                  value={formData.planned_distance || ""}
                  onChange={handleChange}
                />
              </label>
            </div>
            <div className="vehicle-form-row">
              <label>
                Actual Distance
                <input
                  name="actual_distance"
                  value={formData.actual_distance || ""}
                  onChange={handleChange}
                />
              </label>
              <label>
                Fuel Consumed
                <input
                  name="fuel_consumed"
                  value={formData.fuel_consumed || ""}
                  onChange={handleChange}
                />
              </label>
            </div>
            <div className="vehicle-form-row">
              <label>
                Start Odometer
                <input
                  name="start_odometer"
                  value={formData.start_odometer || ""}
                  onChange={handleChange}
                />
              </label>
              <label>
                End Odometer
                <input
                  name="end_odometer"
                  value={formData.end_odometer || ""}
                  onChange={handleChange}
                />
              </label>
            </div>
            <label>
              Status
              <select
                name="status"
                value={formData.status || "Draft"}
                onChange={handleChange}
              >
                <option>Draft</option>
                <option>Dispatched</option>
                <option>Completed</option>
                <option>Cancelled</option>
              </select>
            </label>
            <div className="vehicle-form-buttons">
              <button type="submit" className="save-vehicle-btn">
                Save
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

export default Trip;
