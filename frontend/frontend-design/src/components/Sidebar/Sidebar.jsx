import { NavLink } from "react-router-dom";
import "./Sidebar.css";

function Sidebar() {
  return (
    <div className="sidebar">
      <h2>Fleet System</h2>

      <NavLink to="/dashboard" className="menu-item">
        📊 Dashboard
      </NavLink>

      <NavLink to="/vehicle" className="menu-item">
        🚗 Vehicle
      </NavLink>
    </div>
  );
}

export default Sidebar;