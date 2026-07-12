import "./VehicleCard.css";

function VehicleCard({ vehicle, isSelected, onSelectVehicle }) {
  const statusClass = vehicle.status.toLowerCase().replace(/\s+/g, "-");

  return (
    <button
      type="button"
      className={isSelected ? "vehicle-card selected" : "vehicle-card"}
      onClick={() => onSelectVehicle(vehicle)}
    >
      <img src={vehicle.image} alt={vehicle.name} className="vehicle-image" />

      <div className="vehicle-content">
        <div className="driver-card-header vehicle-card-header">
          <div>
            <h3>{vehicle.name}</h3>
            <p className="driver-role">Fleet Vehicle</p>
          </div>
          <span className={`driver-status-pill ${statusClass}`}>
            {vehicle.status}
          </span>
        </div>

        <div className="driver-details-list">
          <div className="driver-detail-item">
            <span className="driver-detail-label">Number</span>
            <span>{vehicle.number}</span>
          </div>
          <div className="driver-detail-item">
            <span className="driver-detail-label">Type</span>
            <span>{vehicle.type}</span>
          </div>
          <div className="driver-detail-item">
            <span className="driver-detail-label">Driver</span>
            <span>{vehicle.driver}</span>
          </div>
          <div className="driver-detail-item">
            <span className="driver-detail-label">Fuel</span>
            <span>{vehicle.fuel}</span>
          </div>
          <div className="driver-detail-item">
            <span className="driver-detail-label">Mileage</span>
            <span>{vehicle.mileage}</span>
          </div>
        </div>
      </div>
    </button>
  );
}

export default VehicleCard;
