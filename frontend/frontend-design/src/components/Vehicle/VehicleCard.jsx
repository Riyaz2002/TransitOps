import "./VehicleCard.css";

function VehicleCard({ vehicle, isSelected, onSelectVehicle }) {
  return (
    <button
      type="button"
      className={isSelected ? "vehicle-card selected" : "vehicle-card"}
      onClick={() => onSelectVehicle(vehicle)}
    >
      <img
        src={vehicle.image}
        alt={vehicle.name}
        className="vehicle-image"
      />

      <div className="vehicle-content">
        <h3>{vehicle.name}</h3>

        <p>{vehicle.number}</p>

        <p>{vehicle.type}</p>

        <p>{vehicle.driver}</p>

        <p>{vehicle.fuel} fuel</p>

        <span
          className={`status ${vehicle.status
            .toLowerCase()
            .replace(" ", "-")}`}
        >
          {vehicle.status}
        </span>

        <span className="view-btn">Edit Details</span>
      </div>
    </button>
  );
}

export default VehicleCard;
