import VehicleCard from "./VehicleCard";

function VehicleGrid({ vehicles }) {
  return (
    <div className="vehicle-grid">
      {vehicles.map((vehicle) => (
        <VehicleCard
          key={vehicle.id}
          vehicle={vehicle}
        />
      ))}
    </div>
  );
}

export default VehicleGrid;