function VehicleCard({ vehicle }) {
  return (
    <div className="vehicle-card">
      <img src={vehicle.image} alt={vehicle.name} />

      <div className="card-body">
        <h3>{vehicle.name}</h3>

        <p>{vehicle.number}</p>

        <p>{vehicle.driver}</p>

        <span>{vehicle.status}</span>
      </div>
    </div>
  );
}

export default VehicleCard;