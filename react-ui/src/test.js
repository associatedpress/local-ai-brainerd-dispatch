import './App.css';
import React, { useEffect } from 'react';
import { Route, Routes, useLocation, Navigate } from 'react-router-dom';
import HomePage from './components/HomePage/HomePage.js';
import LoginPage from './components/LoginPage/LoginPage.js';

function App() {
  const location = useLocation();
  const session_token = location.state?.session_token;
  const username = location.state?.username;

  useEffect(() => {
    // Check if there is a session token in the local storage
    const storedSessionToken = localStorage.getItem('session_token');
    if (!storedSessionToken) {
      // Redirect the user to the login page if there is no session token
      return <Navigate to="/loginpage" />;
    }
  }, []);

  return (
    <div className="App">
      <Routes>
        <Route
          path="/homepage"
          element={session_token ? <HomePage /> : <Navigate to="/loginpage" />}
        />
        <Route path="/loginpage" element={<LoginPage />} />
      </Routes>
      <header className="App-header"></header>
    </div>
  );
}

export default App;
