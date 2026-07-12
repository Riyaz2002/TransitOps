import { useEffect, useMemo, useState } from "react";
import "../Vehicle/Vehicle.css";
import driversData from "../../data/drivers";
import {
  createDriverApi,
  getDriversApi,
  updateDriverApi,
} from "../../api/driverApi";

const emptyDriver = {
  name: "",
  license: "",
  phone: "",
  vehicle: "",
  status: "Available",
  shift: "Morning",
  experience: "",
  image: "",
};

function Driver({ dataMode }) {
  const [drivers, setDrivers] = useState(driversData);
  const [selectedDriver, setSelectedDriver] = useState(null);
  const [formData, setFormData] = useState(emptyDriver);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortKey, setSortKey] = useState("name");

  const isEditing = Boolean(selectedDriver);
  const isApiMode = dataMode === "api";

  useEffect(() => {
    const loadDrivers = async () => {
      setError("");
      setShowForm(false);
      setSelectedDriver(null);
      setFormData(emptyDriver);

      if (!isApiMode) {
        setDrivers(driversData);
        return;
      }

      setIsLoading(true);
      try {
        const response = await getDriversApi();
        setDrivers(Array.isArray(response) ? response : []);
      } catch {
        setDrivers([]);
        setError("Unable to load API driver records.");
      } finally {
        setIsLoading(false);
      }
    };

    loadDrivers();
  }, [isApiMode]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((currentData) => ({
      ...currentData,
      [name]: value,
    }));
  };

  const handleCreate = () => {
    setSelectedDriver(null);
    setFormData(emptyDriver);
    setShowForm(true);
    setError("");
  };

  const handleSelect = (driver) => {
    setSelectedDriver(driver);
    setFormData(driver);
    setShowForm(true);
    setError("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setIsSaving(true);

    try {
      if (isEditing) {
        if (isApiMode) {
          const updatedDriver = await updateDriverApi(
            selectedDriver.id,
            formData,
          );
          setDrivers((currentDrivers) =>
            currentDrivers.map((driver) =>
              driver.id === selectedDriver.id ? updatedDriver : driver,
            ),
          );
          setSelectedDriver(updatedDriver);
          setFormData(updatedDriver);
          return;
        }

        setDrivers((currentDrivers) =>
          currentDrivers.map((driver) =>
            driver.id === selectedDriver.id
              ? { ...formData, id: selectedDriver.id }
              : driver,
          ),
        );
        return;
      }

      const newDriverPayload = {
        ...formData,
        image:
          formData.image ||
          "https://images.unsplash.com/photo-1500648767791-00dcc994a43e",
      };

      const newDriver = isApiMode
        ? await createDriverApi(newDriverPayload)
        : {
            ...newDriverPayload,
            id: Date.now(),
          };

      setDrivers((currentDrivers) => [newDriver, ...currentDrivers]);
      setSelectedDriver(newDriver);
      setFormData(newDriver);
      setShowForm(true);
    } catch {
      setError("Unable to save driver record.");
    } finally {
      setIsSaving(false);
    }
  };

  const filteredDrivers = useMemo(() => {
    const query = searchTerm.trim().toLowerCase();

    const matches = drivers.filter((driver) => {
      if (!query) {
        return true;
      }

      return [
        driver.name,
        driver.license,
        driver.phone,
        driver.vehicle,
        driver.status,
        driver.shift,
      ]
        .join(" ")
        .toLowerCase()
        .includes(query);
    });

    return [...matches].sort((a, b) => {
      if (sortKey === "status") {
        return a.status.localeCompare(b.status);
      }
      if (sortKey === "shift") {
        return a.shift.localeCompare(b.shift);
      }
      return a.name.localeCompare(b.name);
    });
  }, [searchTerm, sortKey, drivers]);

  const handleDelete = () => {
    if (!selectedDriver) {
      return;
    }

    setDrivers((currentDrivers) =>
      currentDrivers.filter((driver) => driver.id !== selectedDriver.id),
    );
    setSelectedDriver(null);
    setFormData(emptyDriver);
    setShowForm(false);
  };

  return (
    <div className="vehicle-page">
      <div className="vehicle-actions">
        <div className="vehicle-toolbar">
          <p>
            {isLoading
              ? "Loading drivers..."
              : `${filteredDrivers.length} drivers registered`}
            <span className="vehicle-mode-label">
              {isApiMode ? "API Mode" : "Dummy Mode"}
            </span>
          </p>
          <div className="vehicle-filter-bar">
            <input
              type="text"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              placeholder="Search drivers"
            />
            <select
              value={sortKey}
              onChange={(event) => setSortKey(event.target.value)}
            >
              <option value="name">Sort by name</option>
              <option value="status">Sort by status</option>
              <option value="shift">Sort by shift</option>
            </select>
          </div>
        </div>
        <button
          type="button"
          className="create-vehicle-btn"
          onClick={handleCreate}
        >
          Add Driver
        </button>
      </div>

      {error && <p className="vehicle-error">{error}</p>}

      <div className="vehicle-manager">
        <div className="vehicle-grid">
          {filteredDrivers.map((driver) => (
            <article
              key={driver.id}
              className={`vehicle-card driver-card${selectedDriver?.id === driver.id ? " active" : ""}`}
              onClick={() => handleSelect(driver)}
            >
              <img
                src={driver.image}
                alt={driver.name}
                className="vehicle-card-image"
              />
              <div className="vehicle-card-content">
                <div className="driver-card-header">
                  <div>
                    <h3>{driver.name}</h3>
                    <p className="driver-role">Assigned Driver</p>
                  </div>
                  <span
                    className={`driver-status-pill ${driver.status.toLowerCase().replace(/\s+/g, "-")}`}
                  >
                    {driver.status}
                  </span>
                </div>

                <div className="driver-details-list">
                  <div className="driver-detail-item">
                    <span className="driver-detail-label">License</span>
                    <span>{driver.license}</span>
                  </div>
                  <div className="driver-detail-item">
                    <span className="driver-detail-label">Phone</span>
                    <span>{driver.phone}</span>
                  </div>
                  <div className="driver-detail-item">
                    <span className="driver-detail-label">Vehicle</span>
                    <span>{driver.vehicle}</span>
                  </div>
                  <div className="driver-detail-item">
                    <span className="driver-detail-label">Shift</span>
                    <span>{driver.shift}</span>
                  </div>
                  <div className="driver-detail-item">
                    <span className="driver-detail-label">Experience</span>
                    <span>{driver.experience}</span>
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
                <h2>{isEditing ? "Edit Driver" : "Create Driver"}</h2>
                <p>{isEditing ? formData.name : "New record"}</p>
              </div>

              <button
                type="button"
                className="close-form-btn"
                aria-label="Close driver form"
                onClick={() => setShowForm(false)}
              >
                x
              </button>
            </div>

            <label>
              Driver Name
              <input
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Driver name"
                required
              />
            </label>

            <label>
              License Number
              <input
                name="license"
                value={formData.license}
                onChange={handleChange}
                placeholder="DL number"
                required
              />
            </label>

            <label>
              Phone Number
              <input
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="Phone number"
                required
              />
            </label>

            <label>
              Assigned Vehicle
              <input
                name="vehicle"
                value={formData.vehicle}
                onChange={handleChange}
                placeholder="Vehicle name"
                required
              />
            </label>

            <label>
              Status
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
              >
                <option>Available</option>
                <option>On Duty</option>
                <option>Break</option>
              </select>
            </label>

            <div className="vehicle-form-row">
              <label>
                Shift
                <select
                  name="shift"
                  value={formData.shift}
                  onChange={handleChange}
                >
                  <option>Morning</option>
                  <option>Evening</option>
                  <option>Night</option>
                </select>
              </label>

              <label>
                Experience
                <input
                  name="experience"
                  value={formData.experience}
                  onChange={handleChange}
                  placeholder="5 years"
                  required
                />
              </label>
            </div>

            <label>
              Image URL
              <input
                name="image"
                value={formData.image || ""}
                onChange={handleChange}
                placeholder="https://..."
              />
            </label>

            <div className="vehicle-form-buttons">
              <button
                type="submit"
                className="save-vehicle-btn"
                disabled={isSaving}
              >
                {isSaving
                  ? "Saving..."
                  : isEditing
                    ? "Save Changes"
                    : "Create Record"}
              </button>

              {isEditing && (
                <button
                  type="button"
                  className="delete-vehicle-btn"
                  onClick={handleDelete}
                >
                  Delete
                </button>
              )}
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

export default Driver;
