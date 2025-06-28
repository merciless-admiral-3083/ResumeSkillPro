/**
 * Component for handling file uploads
 * @param {Object} props - Component props
 * @param {Function} props.onFileUpload - Callback function when file is uploaded
 */
const UploadForm = ({ onFileUpload }) => {
  const [isDragging, setIsDragging] = React.useState(false);
  const [file, setFile] = React.useState(null);
  const fileInputRef = React.useRef(null);

  /**
   * Handle file selection
   * @param {Event} e - File input change event
   */
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
    } else {
      alert('Please select a valid PDF file.');
    }
  };

  /**
   * Handle file submission
   * @param {Event} e - Form submit event
   */
  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      onFileUpload(file);
    } else {
      alert('Please select a PDF file before submitting.');
    }
  };

  /**
   * Handle click on the upload area
   */
  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  /**
   * Handle drag over event
   * @param {Event} e - Drag event
   */
  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  /**
   * Handle drag leave event
   * @param {Event} e - Drag event
   */
  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  /**
   * Handle drop event
   * @param {Event} e - Drop event
   */
  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === 'application/pdf') {
      setFile(droppedFile);
    } else {
      alert('Please drop a valid PDF file.');
    }
  };

  return (
    <div className="text-center">
      <div 
        className={`upload-area mb-4 ${isDragging ? 'dragging' : ''}`}
        onClick={handleUploadClick}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="upload-icon mb-3">
          <i className="fas fa-file-pdf fa-3x"></i>
        </div>
        <h4>Drag and drop your resume</h4>
        <p className="text-muted">or click to select a PDF file</p>
        
        <input 
          type="file" 
          className="d-none" 
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf"
        />

        {file && (
          <div className="selected-file mt-3">
            <div className="alert alert-info d-inline-block">
              <i className="fas fa-check-circle me-2"></i>
              {file.name}
            </div>
          </div>
        )}
      </div>

      <button 
        className="btn btn-primary btn-lg"
        onClick={handleSubmit}
        disabled={!file}
      >
        <i className="fas fa-magic me-2"></i> Extract Skills
      </button>

      <div className="mt-4">
        <p className="text-muted small">
          Supported format: PDF only. Maximum size: 10MB.
        </p>
      </div>
    </div>
  );
};
