import './App.css';
import React, { useState } from 'react'
import { Route, Routes, Navigate } from 'react-router-dom'
import HomePage from './components/HomePage/HomePage.js'
import LoginPage from './components/LoginPage/LoginPage.js'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <div className="App">
      <Routes>
        <Route path="/homepage" element={isLoggedIn ? <HomePage /> : <Navigate to="/loginpage" />} />
        <Route path="/loginpage" element={<LoginPage onLogin={handleLogin} />} />
        <Route path="/*" element={<Navigate to="/homepage" />} />
      </Routes>
      <header className="App-header">
      </header>
    </div>
  );
}

export default App;
