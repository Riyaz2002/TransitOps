import { Routes, Route } from "react-router-dom";

import Login from "../pages/Login/Login";
import Dashboard from "../pages/Dashboard/Dashboard";
import Vehicle from "../pages/Vehicle/Vehicle";
import Driver from "../pages/Driver/Driver";
import Layout from "../layouts/Layout";

function AppRoutes({ darkMode, setDarkMode, dataMode, setDataMode }) {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <Login
            darkMode={darkMode}
            setDarkMode={setDarkMode}
            dataMode={dataMode}
            setDataMode={setDataMode}
          />
        }
      />

      <Route element={<Layout darkMode={darkMode} setDarkMode={setDarkMode} />}>
        <Route path="/dashboard" element={<Dashboard />} />

        <Route path="/vehicle" element={<Vehicle dataMode={dataMode} />} />

        <Route path="/driver" element={<Driver />} />
      </Route>
    </Routes>
  );
}

export default AppRoutes;
