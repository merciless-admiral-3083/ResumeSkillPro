/**
 * Main App component that coordinates the resume skill extraction app
 */
const App = () => {
  const [skills, setSkills] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [fileName, setFileName] = React.useState(null);

  /**
   * Handle file upload and skill extraction
   * @param {File} file - The uploaded PDF file
   */
  const handleFileUpload = async (file) => {
    setFileName(file.name);
    setLoading(true);
    setError(null);
    setSkills(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/extract-skills', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      if (response.data.success) {
        setSkills(response.data.skills);
      } else {
        setError(response.data.error || 'An error occurred while processing your resume.');
      }
    } catch (err) {
      console.error('Error uploading file:', err);
      setError(err.response?.data?.error || 'Failed to upload file. Please try again.');
    } finally {
      setLoading(false);
    }
  };

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
                <UploadForm onFileUpload={handleFileUpload} />
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
};

// Render the App component
ReactDOM.render(<App />, document.getElementById('root'));
