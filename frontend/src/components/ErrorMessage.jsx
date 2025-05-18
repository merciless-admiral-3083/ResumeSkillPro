import React from 'react';
import '../styles/ErrorMessage.css';

/**
 * Component to display error messages
 * @param {Object} props - Component props
 * @param {string} props.message - Error message to display
 * @param {Function} props.onReset - Function to reset the application state
 */
const ErrorMessage = ({ message, onReset }) => {
  return (
    <div className="text-center py-4">
      <div className="error-icon mb-3">
        <i className="fas fa-exclamation-circle text-danger fa-3x"></i>
      </div>
      
      <h4 className="text-danger">Error Processing Resume</h4>
      
      <div className="alert alert-danger mt-3">
        {message || "An unexpected error occurred. Please try again."}
      </div>
      
      <p className="mb-4">
        Please make sure your file is a valid PDF and try again.
      </p>
      
      <button 
        className="btn btn-outline-primary"
        onClick={onReset}
      >
        <i className="fas fa-redo me-2"></i> Try Again
      </button>
    </div>
  );
};

export default ErrorMessage;