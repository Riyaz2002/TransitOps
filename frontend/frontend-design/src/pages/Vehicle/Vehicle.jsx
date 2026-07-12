import { useEffect, useMemo, useState } from "react";
import "./Vehicle.css";
import VehicleGrid from "../../components/Vehicle/VehicleGrid";
import vehicleData from "../../data/vehicles";
import {
  createVehicleApi,
  deleteVehicleApi,
  getVehiclesApi,
  updateVehicleApi,
} from "../../api/vehicleApi";

const emptyVehicle = {
  name: "",
  number: "",
  type: "",
  driver: "",
  status: "Available",
  fuel: "",
  mileage: "",
  image: "",
};

function Vehicle({ dataMode }) {
  const [vehicles, setVehicles] = useState(vehicleData);
  const [selectedVehicle, setSelectedVehicle] = useState(null);
  const [formData, setFormData] = useState(emptyVehicle);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortKey, setSortKey] = useState("name");

  const isEditing = Boolean(selectedVehicle);
  const isApiMode = dataMode === "api";

  useEffect(() => {
    const loadVehicles = async () => {
      setError("");
      setShowForm(false);
      setSelectedVehicle(null);
      setFormData(emptyVehicle);

      if (!isApiMode) {
        setVehicles(vehicleData);
        return;
      }

      setIsLoading(true);

      try {
        const response = await getVehiclesApi();
        const apiVehicles = Array.isArray(response)
          ? response
          : response.results || [];
        setVehicles(apiVehicles);
      } catch {
        setVehicles([]);
        setError("Unable to load API vehicle records.");
      } finally {
        setIsLoading(false);
      }
    };

    loadVehicles();
  }, [isApiMode]);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((currentData) => ({
      ...currentData,
      [name]: value,
    }));
  };

  const handleCreate = () => {
    setSelectedVehicle(null);
    setFormData(emptyVehicle);
    setShowForm(true);
    setError("");
  };

  const handleSelect = (vehicle) => {
    setSelectedVehicle(vehicle);
    setFormData(vehicle);
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
          const updatedVehicle = await updateVehicleApi(
            selectedVehicle.id,
            formData,
          );

          setVehicles((currentVehicles) =>
            currentVehicles.map((vehicle) =>
              vehicle.id === selectedVehicle.id ? updatedVehicle : vehicle,
            ),
          );
          setSelectedVehicle(updatedVehicle);
          setFormData(updatedVehicle);
          return;
        }

        setVehicles((currentVehicles) =>
          currentVehicles.map((vehicle) =>
            vehicle.id === selectedVehicle.id
              ? { ...formData, id: selectedVehicle.id }
              : vehicle,
          ),
        );
        return;
      }

      const newVehiclePayload = {
        ...formData,
        image:
          formData.image ||
          "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7",
      };

      const newVehicle = isApiMode
        ? await createVehicleApi(newVehiclePayload)
        : {
            ...newVehiclePayload,
            id: Date.now(),
          };

      setVehicles((currentVehicles) => [newVehicle, ...currentVehicles]);
      setSelectedVehicle(newVehicle);
      setFormData(newVehicle);
      setShowForm(true);
    } catch {
      setError("Unable to save vehicle record.");
    } finally {
      setIsSaving(false);
    }
  };

  const filteredVehicles = useMemo(() => {
    const query = searchTerm.trim().toLowerCase();

    const matches = vehicles.filter((vehicle) => {
      if (!query) {
        return true;
      }

      return [
        vehicle.name,
        vehicle.number,
        vehicle.driver,
        vehicle.type,
        vehicle.status,
      ]
        .join(" ")
        .toLowerCase()
        .includes(query);
    });

    return [...matches].sort((a, b) => {
      if (sortKey === "status") {
        return a.status.localeCompare(b.status);
      }
      if (sortKey === "driver") {
        return a.driver.localeCompare(b.driver);
      }
      return a.name.localeCompare(b.name);
    });
  }, [searchTerm, sortKey, vehicles]);

  const handleDelete = async () => {
    if (!selectedVehicle) {
      return;
    }

    setError("");
    setIsSaving(true);

    try {
      if (isApiMode) {
        await deleteVehicleApi(selectedVehicle.id);
      }

      setVehicles((currentVehicles) =>
        currentVehicles.filter((vehicle) => vehicle.id !== selectedVehicle.id),
      );
      setSelectedVehicle(null);
      setFormData(emptyVehicle);
      setShowForm(false);
    } catch {
      setError("Unable to delete vehicle record.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="vehicle-page">
      <div className="vehicle-actions">
        <div className="vehicle-toolbar">
          <p>
            {isLoading
              ? "Loading records..."
              : `${filteredVehicles.length} records`}
            <span className="vehicle-mode-label">
              {isApiMode ? "API Mode" : "Dummy Mode"}
            </span>
          </p>
          <div className="vehicle-filter-bar">
            <input
              type="text"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              placeholder="Search vehicles"
            />
            <select
              value={sortKey}
              onChange={(event) => setSortKey(event.target.value)}
            >
              <option value="name">Sort by name</option>
              <option value="status">Sort by status</option>
              <option value="driver">Sort by driver</option>
            </select>
          </div>
        </div>
        <button
          type="button"
          className="create-vehicle-btn"
          onClick={handleCreate}
        >
          Add Vehicle
        </button>
      </div>

      {error && <p className="vehicle-error">{error}</p>}

      <div className="vehicle-manager">
        <VehicleGrid
          vehicles={filteredVehicles}
          selectedVehicleId={selectedVehicle?.id}
          onSelectVehicle={handleSelect}
        />

        {showForm && (
          <form className="vehicle-form" onSubmit={handleSubmit}>
            <div className="vehicle-form-header">
              <div>
                <h2>{isEditing ? "Edit Vehicle" : "Create Vehicle"}</h2>
                <p>{isEditing ? formData.number : "New record"}</p>
              </div>

              <button
                type="button"
                className="close-form-btn"
                aria-label="Close vehicle form"
                onClick={() => setShowForm(false)}
              >
                x
              </button>
            </div>

            <label>
              Vehicle Name
              <input
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Toyota Fortuner"
                required
              />
            </label>

            <label>
              Vehicle Number
              <input
                name="number"
                value={formData.number}
                onChange={handleChange}
                placeholder="TN01AB1234"
                required
              />
            </label>

            <label>
              Type
              <input
                name="type"
                value={formData.type}
                onChange={handleChange}
                placeholder="SUV"
                required
              />
            </label>

            <label>
              Driver
              <input
                name="driver"
                value={formData.driver}
                onChange={handleChange}
                placeholder="Driver name"
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
                <option>In Use</option>
                <option>Maintenance</option>
              </select>
            </label>

            <div className="vehicle-form-row">
              <label>
                Fuel
                <input
                  name="fuel"
                  value={formData.fuel}
                  onChange={handleChange}
                  placeholder="78%"
                  required
                />
              </label>

              <label>
                Mileage
                <input
                  name="mileage"
                  value={formData.mileage}
                  onChange={handleChange}
                  placeholder="18 km/L"
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
                  disabled={isSaving}
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

export default Vehicle;
