import VehicleCard from "./VehicleCard";

function VehicleGrid({ vehicles, selectedVehicleId, onSelectVehicle }) {
  return (
    <div className="vehicle-grid">
      {vehicles.map((vehicle) => (
        <VehicleCard
          key={vehicle.id}
          vehicle={vehicle}
          isSelected={vehicle.id === selectedVehicleId}
          onSelectVehicle={onSelectVehicle}
        />
      ))}
    </div>
  );
}

export default VehicleGrid;
