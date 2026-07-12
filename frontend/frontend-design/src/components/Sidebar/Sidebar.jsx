import { NavLink, useNavigate } from "react-router-dom";
import "./Sidebar.css";

const menuItems = [
  {
    label: "Dashboard",
    path: "/dashboard",
    icon: "D",
  },
  {
    label: "Vehicle",
    path: "/vehicle",
    icon: "V",
  },
  {
    label: "Driver",
    path: "/driver",
    icon: "DR",
  },
  {
    label: "Trip",
    path: "/trip",
    icon: "TR",
  },
];

function Sidebar({ darkMode, hidden, setHidden }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("data_mode");
    navigate("/");
  };

  return (
    <div
      className={`${darkMode ? "sidebar dark" : "sidebar"}${hidden ? " hidden" : ""}`}
    >
      <button
        type="button"
        className="sidebar-toggle"
        aria-label={hidden ? "Show menu" : "Hide menu"}
        aria-expanded={!hidden}
        onClick={() => setHidden(!hidden)}
      >
        {hidden ? ">" : "<"}
      </button>

      <div className="sidebar-header">
        <h2>Fleet Registry</h2>
        <p>Menu</p>
      </div>

      <nav className="menu-grid">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `menu-item${isActive ? " active" : ""}`
            }
          >
            <span className="menu-icon">{item.icon}</span>
            <span className="menu-label">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <button type="button" className="logout-btn" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
}

export default Sidebar;
