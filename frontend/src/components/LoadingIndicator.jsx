import React from 'react';
import '../styles/LoadingIndicator.css';

const LoadingIndicator = () => {
  return (
    <div className="text-center py-5">
      <div className="spinner-border text-primary mb-3" role="status" style={{ width: '3rem', height: '3rem' }}>
        <span className="visually-hidden">Loading...</span>
      </div>
      <h4 className="mt-3">Analyzing your resume...</h4>
      <p className="text-muted">
        We're extracting skills from your PDF using NLP. This may take a moment.
      </p>
      
      <div className="progress mt-4" style={{ height: '10px' }}>
        <div 
          className="progress-bar progress-bar-striped progress-bar-animated" 
          role="progressbar" 
          style={{ width: '100%' }}
        ></div>
      </div>
    </div>
  );
};

export default LoadingIndicator;