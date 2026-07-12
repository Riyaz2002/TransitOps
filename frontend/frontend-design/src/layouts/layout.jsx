import { useEffect, useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "../components/Sidebar/Sidebar";
import "./Layout.css";

const pageTitles = {
  "/dashboard": "Dashboard",
  "/vehicle": "Vehicles",
};

function Layout({ darkMode, setDarkMode }) {
  const location = useLocation();
  const pageTitle = pageTitles[location.pathname] || "TransitOps";
  const [sidebarHidden, setSidebarHidden] = useState(false);

  useEffect(() => {
    document.title = `${pageTitle} | Fleet Registry`;
  }, [pageTitle]);

  return (
    <div className={darkMode ? "layout dark" : "layout"}>
      <Sidebar
        darkMode={darkMode}
        hidden={sidebarHidden}
        setHidden={setSidebarHidden}
      />

      <div className="layout-content">
        <div className="topbar">
          <div className="page-title">
            <h1>{pageTitle}</h1>
          </div>

          <button
            type="button"
            className="theme-toggle"
            aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}
            aria-pressed={darkMode}
            onClick={() => setDarkMode(!darkMode)}
          >
            <span className="theme-toggle-track">
              <span className="theme-toggle-thumb" />
            </span>
            <span className="theme-toggle-text">
              {darkMode ? "Light" : "Dark"}
            </span>
          </button>
        </div>

        <div
          key={location.pathname}
          className="page-transition"
        >
          <Outlet />
        </div>
      </div>
    </div>
  );
}

export default Layout;
