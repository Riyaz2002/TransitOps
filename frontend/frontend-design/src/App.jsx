import { useState } from "react";
import AppRoutes from "./routes/AppRoutes";

function App() {
  const [darkMode, setDarkMode] = useState(false);

  return (
    <AppRoutes
      darkMode={darkMode}
      setDarkMode={setDarkMode}
    />
  );
}

export default App;