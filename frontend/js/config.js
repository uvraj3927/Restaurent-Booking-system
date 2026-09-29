/**
 * Pyrites Grill Frontend Configuration
 * Dynamically resolves API base URL based on environment.
 */

// Initialize API_BASE globally on window object to prevent redeclaration errors
if (typeof window.API_BASE === 'undefined') {
  window.API_BASE = "http://44.200.253.83:5000/api";
}

// Alternative CONFIG object for future extensibility
const CONFIG = {
  API_BASE: window.API_BASE
};
