import { Routes, Route } from "react-router-dom";
import Login from "../pages/Login/Login";
import Dashboard from "../pages/Dashboard/Dashboard";
import Vehicle from "../pages/Vehicle/Vehicle.jsx";
import Layout from "../layouts/Layout";

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
             <Route element={<Layout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/vehicle" element={<Vehicle />} />
      </Route>
    </Routes>
  );
}
export default AppRoutes;