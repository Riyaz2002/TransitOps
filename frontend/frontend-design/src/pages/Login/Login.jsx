import { useState } from "react";
import "./Login.css";
import { useNavigate } from "react-router-dom";



function Login() {
  const [darkMode, setDarkMode] = useState(false);
  const navigate = useNavigate();
  const handleLogin = () => {
      navigate("/dashboard");
  };
  return (
    <div className={darkMode ? "login-page dark" : "login-page"}>
      <button
        className="theme-btn"
        onClick={() => setDarkMode(!darkMode)}
      >
        {darkMode ? "☀ Light" : "🌙 Dark"}
      </button>

      <div className="login-card">

        <h1>Welcome Back</h1>
        <p>Please sign in to continue</p>

        <form>

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

          {/* <div className="input-group">
            <label>Role</label>

            <select>
              <option>Select Role</option>
              <option>Fleet Manager</option>
              <option>Driver</option>
              <option>Safety Officer</option>
              <option>Financial Analyst</option>
            </select>

          </div> */}

          <div className="login-options">

            <label>
              <input type="checkbox" />
              Remember Me
            </label>

            <a href="/">Forgot Password?</a>

          </div>

          <button className="login-btn"  onClick={handleLogin}>
            Sign In
          </button>

        </form>

      </div>
    </div>
  );
}

export default Login;