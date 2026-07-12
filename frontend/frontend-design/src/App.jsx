import { useState } from "react";
import AppRoutes from "./routes/AppRoutes";

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [dataMode, setDataMode] = useState("dummy");

  return (
    <AppRoutes
      darkMode={darkMode}
      setDarkMode={setDarkMode}
      dataMode={dataMode}
      setDataMode={setDataMode}
    />
  );
}

export default App;
