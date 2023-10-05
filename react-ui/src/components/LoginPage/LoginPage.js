
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

function LoginPage({ onLogin }) {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const baseuri = process.env.REACT_APP_BACKEND_SERVER_URL;

  useEffect(() => {
    const sessionToken = localStorage.getItem('session_token');
    if (sessionToken) {
      onLogin();
      navigate('/homepage');
      document.getElementsByClassName('App-header')[0].style.display = 'none';
    }
  }, []); // Empty dependency array ensures this effect runs only once

  function handleSubmit(event) {
    event.preventDefault();
    setErrorMessage(''); // Clear any previous error message
    console.log("Login Submit Handler");
    console.log(baseuri);
    console.log('Submitting:', username, password);
    axios
      .post(baseuri + `/login`, {
        username: username,
        password: password,
      })
      .then((response) => {
        console.log(response.data.response.session_token);

        localStorage.setItem('session_token', response.data.response.session_token);
        localStorage.setItem('username', response.data.response.username);

        navigate('/homepage', { state: { "session_token": response.data.response.session_token, "username": response.data.response.username } });
        document.getElementsByClassName('App-header')[0].style.display = 'none';
        onLogin(); // Call the onLogin callback to set isLoggedIn to true
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
          setErrorMessage('Username or password is incorrect.'); // Set the error message
        }
      });
  }

  return (
    <div className="loginpage">
      <h1>Public Safety Reporting System</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>
        <br />
        <label>
          Password:
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <br />
        <button type="submit">Login</button>
      </form>
      {errorMessage && <p className="error-message">{errorMessage}</p>} 
    </div>
  );
}

export default LoginPage;
