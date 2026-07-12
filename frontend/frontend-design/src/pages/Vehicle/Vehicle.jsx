import "./Vehicle.css";
import VehicleGrid from "../../components/Vehicle/VehicleGrid";
import vehicles from "../../data/vehicles";

function Vehicle() {
  return (
    <div className="vehicle-page">
      <VehicleGrid vehicles={vehicles} />
    </div>
  );
}

export default Vehicle;
