import "./VehicleCard.css";

function VehicleCard({ vehicle }) {
  return (
    <div className="vehicle-card">
      <img
        src={vehicle.image}
        alt={vehicle.name}
        className="vehicle-image"
      />

      <div className="vehicle-content">
        <h3>{vehicle.name}</h3>

        <p>{vehicle.number}</p>

        <p>{vehicle.driver}</p>

        <span
          className={`status ${vehicle.status
            .toLowerCase()
            .replace(" ", "-")}`}
        >
          {vehicle.status}
        </span>

        <button className="view-btn">View Details</button>
      </div>
    </div>
  );
}

export default VehicleCard;