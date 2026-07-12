import "./Login.css";
import { useNavigate } from "react-router-dom";

function Login({ darkMode, setDarkMode }) {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    navigate("/dashboard");
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

        <form onSubmit={handleLogin}>
          <div className="input-group">
            <label>Email</label>

            <input
              type="email"
              placeholder="Enter your email"
            />
          </div>

          <div className="input-group">
            <label>Password</label>

            <input
              type="password"
              placeholder="Enter your password"
            />
          </div>

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
          >
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
