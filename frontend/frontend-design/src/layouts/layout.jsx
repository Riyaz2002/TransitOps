import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar/Sidebar";

function Layout() {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <Sidebar />

      <main style={{ flex: 1, padding: "20px" }}>
        <Outlet />
      </main>
    </div>
  );
}

export default Layout;