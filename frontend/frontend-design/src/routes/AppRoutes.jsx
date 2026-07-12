import { Routes, Route } from "react-router-dom";

import Login from "../pages/Login/Login";
import Dashboard from "../pages/Dashboard/Dashboard";
import Vehicle from "../pages/Vehicle/Vehicle";
import Layout from "../layouts/Layout";

function AppRoutes({ darkMode, setDarkMode }) {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <Login
            darkMode={darkMode}
            setDarkMode={setDarkMode}
          />
        }
      />

      <Route
        element={
          <Layout
            darkMode={darkMode}
            setDarkMode={setDarkMode}
          />
        }
      >
        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/vehicle"
          element={<Vehicle />}
        />
      </Route>
    </Routes>
  );
}

export default AppRoutes;
