import { useState } from "react";
import "./Login.css";
import { useNavigate } from "react-router-dom";
import { loginApi, registerApi } from "../../api/authApi";

function Login({ darkMode, setDarkMode, dataMode, setDataMode }) {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({
    email: "",
    password: "",
  });
  const [signupData, setSignupData] = useState({
    full_name: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSignupMode, setIsSignupMode] = useState(false);

  const isApiMode = dataMode === "api";

  const handleChange = (event) => {
    const { name, value } = event.target;

    setCredentials((currentCredentials) => ({
      ...currentCredentials,
      [name]: value,
    }));
  };

  const handleSignupChange = (event) => {
    const { name, value } = event.target;

    setSignupData((currentSignupData) => ({
      ...currentSignupData,
      [name]: value,
    }));
  };

  const handleLogin = async (event) => {
    event.preventDefault();
    setError("");
    setSuccessMessage("");

    if (!isApiMode) {
      localStorage.setItem("data_mode", "dummy");
      navigate("/dashboard");
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await loginApi(credentials);
      const token = response.access_token || response.access || response.token;

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

  const handleSignup = async (event) => {
    event.preventDefault();
    setError("");
    setSuccessMessage("");

    if (!isApiMode) {
      setSuccessMessage("Signup is available in API mode only.");
      return;
    }

    setIsSubmitting(true);

    try {
      await registerApi(signupData);
      setSuccessMessage("Account created successfully. You can sign in now.");
      setSignupData({ full_name: "", email: "", password: "" });
      setIsSignupMode(false);
    } catch {
      setError("Signup failed. Please try a different email.");
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
        <span className="theme-toggle-text">{darkMode ? "Light" : "Dark"}</span>
      </button>

      <div className="login-card">
        <h1>{isSignupMode ? "Create Account" : "Welcome Back"}</h1>
        <p>
          {isSignupMode
            ? "Register to continue with the API"
            : "Please sign in to continue"}
        </p>

        <div className="mode-toggle">
          <button
            type="button"
            className={
              dataMode === "dummy" ? "mode-option active" : "mode-option"
            }
            onClick={() => setDataMode("dummy")}
          >
            Dummy Data
          </button>
          <button
            type="button"
            className={
              dataMode === "api" ? "mode-option active" : "mode-option"
            }
            onClick={() => setDataMode("api")}
          >
            API
          </button>
        </div>

        {isSignupMode ? (
          <form onSubmit={handleSignup}>
            <div className="input-group">
              <label>Full Name</label>
              <input
                type="text"
                name="full_name"
                value={signupData.full_name}
                onChange={handleSignupChange}
                placeholder="Enter your full name"
                required={isApiMode}
              />
            </div>

            <div className="input-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={signupData.email}
                onChange={handleSignupChange}
                placeholder="Enter your email"
                required={isApiMode}
              />
            </div>

            <div className="input-group">
              <label>Password</label>
              <input
                type="password"
                name="password"
                value={signupData.password}
                onChange={handleSignupChange}
                placeholder="Create a password"
                required={isApiMode}
              />
            </div>

            {error && <p className="login-error">{error}</p>}
            {successMessage && (
              <p className="login-success">{successMessage}</p>
            )}

            <button type="submit" className="login-btn" disabled={isSubmitting}>
              {isSubmitting ? "Creating Account..." : "Create Account"}
            </button>

            <p className="auth-switch-text">
              Already have an account?{" "}
              <button
                type="button"
                className="auth-switch-link"
                onClick={() => setIsSignupMode(false)}
              >
                Sign In
              </button>
            </p>
          </form>
        ) : (
          <form onSubmit={handleLogin}>
            <div className="input-group">
              <label>Email</label>

              <input
                type="email"
                name="email"
                value={credentials.email}
                onChange={handleChange}
                placeholder={
                  isApiMode ? "Enter your API email" : "Dummy mode email"
                }
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
                placeholder={
                  isApiMode ? "Enter your API password" : "Dummy mode password"
                }
                required={isApiMode}
              />
            </div>

            {error && <p className="login-error">{error}</p>}
            {successMessage && (
              <p className="login-success">{successMessage}</p>
            )}

            <div className="login-options">
              <label>
                <input type="checkbox" />
                Remember Me
              </label>

              <a href="/">Forgot Password?</a>
            </div>

            <button type="submit" className="login-btn" disabled={isSubmitting}>
              {isSubmitting ? "Signing In..." : "Sign In"}
            </button>

            <p className="auth-switch-text">
              Don&apos;t have an account?{" "}
              <button
                type="button"
                className="auth-switch-link"
                onClick={() => setIsSignupMode(true)}
              >
                Sign Up
              </button>
            </p>
          </form>
        )}
      </div>
    </div>
  );
}

export default Login;
