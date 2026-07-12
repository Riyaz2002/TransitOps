import { useState } from "react";
import "./Login.css";
import { useNavigate } from "react-router-dom";
import { loginApi } from "../../api/authApi";

function Login({ darkMode, setDarkMode, dataMode, setDataMode }) {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const isApiMode = dataMode === "api";

  const handleChange = (event) => {
    const { name, value } = event.target;

    setCredentials((currentCredentials) => ({
      ...currentCredentials,
      [name]: value,
    }));
  };

  const handleLogin = async (event) => {
    event.preventDefault();
    setError("");

    if (!isApiMode) {
      localStorage.setItem("data_mode", "dummy");
      navigate("/dashboard");
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await loginApi(credentials);
      const token = response.access || response.access_token || response.token;

      if (token) {
        localStorage.setItem("access_token", token);
      }

      localStorage.setItem("data_mode", "api");
      navigate("/dashboard");
    } catch {
      setError("API login failed. Please check backend and credentials.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={darkMode ? "login-page dark" : "login-page"}>
      <button
        type="button"
        className="theme-toggle login-theme-toggle"
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

      <div className="login-card">
        <h1>Welcome Back</h1>
        <p>Please sign in to continue</p>

        <div className="mode-toggle">
          <button
            type="button"
            className={dataMode === "dummy" ? "mode-option active" : "mode-option"}
            onClick={() => setDataMode("dummy")}
          >
            Dummy Data
          </button>
          <button
            type="button"
            className={dataMode === "api" ? "mode-option active" : "mode-option"}
            onClick={() => setDataMode("api")}
          >
            API
          </button>
        </div>

        <form onSubmit={handleLogin}>
          <div className="input-group">
            <label>Email</label>

            <input
              type="email"
              name="email"
              value={credentials.email}
              onChange={handleChange}
              placeholder={isApiMode ? "Enter your API email" : "Dummy mode email"}
              required={isApiMode}
            />
          </div>

          <div className="input-group">
            <label>Password</label>

            <input
              type="password"
              name="password"
              value={credentials.password}
              onChange={handleChange}
              placeholder={isApiMode ? "Enter your API password" : "Dummy mode password"}
              required={isApiMode}
            />
          </div>

          {error && <p className="login-error">{error}</p>}

          <div className="login-options">
            <label>
              <input type="checkbox" />
              Remember Me
            </label>

            <a href="/">Forgot Password?</a>
          </div>

          <button
            type="submit"
            className="login-btn"
            disabled={isSubmitting}
          >
            {isSubmitting ? "Signing In..." : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
