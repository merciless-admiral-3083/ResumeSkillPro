import axios from 'axios';

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-production-api-url.com/api' 
  : '/api';

/**
 * Upload resume and extract skills
 * @param {File} file - The PDF file to upload
 * @returns {Promise} - Response with extracted skills
 */
export const uploadResume = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_BASE_URL}/extract-skills`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    if (response.data.success) {
      return {
        success: true,
        skills: response.data.skills
      };
    } else {
      throw new Error(response.data.error || 'Failed to extract skills');
    }
  } catch (error) {
    console.error('API Error:', error);
    const errorMessage = error.response?.data?.error || error.message || 'An unexpected error occurred';
    throw new Error(errorMessage);
  }
};

/**
 * Health check for the API
 * @returns {Promise} - Response with API health status
 */
export const checkApiHealth = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  } catch (error) {
    console.error('API Health Check Error:', error);
    throw error;
  }
};