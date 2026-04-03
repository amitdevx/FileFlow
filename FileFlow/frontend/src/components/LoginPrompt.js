import React from 'react';
import './LoginPrompt.css';

function LoginPrompt() {
  return (
    <div className="login-prompt">
      <div className="login-prompt-content">
        <i className="fas fa-lock"></i>
        <h2>Authentication Required</h2>
        <p>You need to be logged in to access the file manager.</p>
        <div className="login-buttons">
          <a href="/login" className="btn btn-primary">
            <i className="fas fa-sign-in-alt"></i> Login
          </a>
          <a href="/signup" className="btn btn-secondary">
            <i className="fas fa-user-plus"></i> Sign Up
          </a>
        </div>
      </div>
    </div>
  );
}

export default LoginPrompt;
