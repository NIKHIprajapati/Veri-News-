import { useEffect, useState } from "react";
import { Link, NavLink } from "react-router-dom";

export default function Header() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("vn_theme") || "light";
  });

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("vn_theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  };

  return (
    <header className="site-header">
      <div className="container site-header__inner">
        <Link to="/" className="brand" aria-label="VeriNews home">
          <img src="/logo.png" alt="VeriNews logo" />
          <span className="brand__text">
            <span className="brand__name">VeriNews</span>
            <span className="brand__tag">Multi-Source News Verification Platform</span>
          </span>
        </Link>

        <div className="header-actions">
          <nav className="nav" aria-label="Main">
            <NavLink to="/" end>Home</NavLink>
            <NavLink to="/about">About</NavLink>
          </nav>
          <button
            type="button"
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
            title={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
          >
            {theme === "dark" ? "☀ Light" : "☾ Dark"}
          </button>
        </div>
      </div>
    </header>
  );
}
