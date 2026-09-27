/**
 * Pyrites Grill Frontend Configuration
 * Dynamically resolves API base URL based on environment.
 */
/*const CONFIG = {
  // If hosted on EC2 or local Flask server, relative path '/api' works seamlessly.
  // For standalone frontend files opened via file:// or separate host, fallback to http://localhost:5000/api
  API_BASE_URL: (window.location.protocol === 'file:' || window.location.port === '3000' || window.location.port === '8080')
    ? 'http://localhost:5000/api'
    : '/api'
};
*/
const API_BASE = "http://44.200.253.83:5000";
