import vehicles from "../../data/vehicles";
import VehicleGrid from "../../components/Vehicle/VehicleGrid";

function Vehicle() {
  return (
    <div>
      <h1>Vehicle Management</h1>

      <VehicleGrid vehicles={vehicles} />
    </div>
  );
}

export default Vehicle;