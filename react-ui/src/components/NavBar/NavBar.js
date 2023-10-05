import React from "react";
import './NavBar.css';
import { useNavigate } from 'react-router-dom';

const NavBar = (props) => {
  const username = localStorage.getItem('username');
  const session_token = localStorage.getItem('session_token');
  const navigate = useNavigate();

  function handleLogout() {
    localStorage.removeItem('session_token');
    localStorage.removeItem('username');
    navigate('/loginpage');
  }
  
  return (
    <nav className="navbar">
      <div className = "navbar-left">
        <p>Public Safety Reporting System</p>
      </div>
      
      <div className="navbar-right">
        <span className="username">Logged in {username}</span>
        <button className="logout-btn" onClick={handleLogout}>Logout</button>
      </div>
    </nav>
  );
};

export default NavBar;
