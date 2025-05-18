import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import SkillsList from './components/SkillsList';
import LoadingIndicator from './components/LoadingIndicator';
import ErrorMessage from './components/ErrorMessage';
import './styles/App.css';

/**
 * Main App component that coordinates the resume skill extraction app
 */
function App() {
  const [skills, setSkills] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fileName, setFileName] = useState(null);

  /**
   * Reset the app state
   */
  const handleReset = () => {
    setSkills(null);
    setError(null);
    setFileName(null);
  };

  return (
    <div className="container my-5">
      <header className="text-center mb-5">
        <h1 className="display-4">Resume Skill Extractor</h1>
        <p className="lead">Upload your resume to instantly extract key skills</p>
      </header>

      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="card bg-dark shadow-sm">
            <div className="card-body">
              {!skills && !loading && (
                <UploadForm 
                  setSkills={setSkills}
                  setLoading={setLoading}
                  setError={setError}
                  setFileName={setFileName}
                />
              )}

              {loading && <LoadingIndicator />}

              {error && <ErrorMessage message={error} onReset={handleReset} />}

              {skills && (
                <div>
                  <div className="mb-4 text-center">
                    <h3>Skills Extracted from: {fileName}</h3>
                    <p className="text-muted">
                      Here are the key skills identified in your resume
                    </p>
                  </div>
                  
                  <SkillsList skills={skills} />

                  <div className="text-center mt-4">
                    <button 
                      className="btn btn-secondary" 
                      onClick={handleReset}
                    >
                      <i className="fas fa-undo me-2"></i> Upload Another Resume
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <footer className="mt-5 text-center text-muted">
        <p>Resume Skill Extractor using React, Flask, and NLP</p>
      </footer>
    </div>
  );
}

export default App;