import axios from "axios";

// Create a single axios instance with the correct base URL
// NOTE: We do not use localhost here to ensure consistency with the deployed backend.
const API = axios.create({
  baseURL: "https://chemical-equipment-ituh.onrender.com/api/",
  headers: {
    "Content-Type": "application/json",
  },
});

// Request Interceptor: Attach the token if it exists
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor: Handle global errors like 401 Unauthorized
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.warn("Unauthorized! Clearing token and redirecting to login.");
      localStorage.removeItem("token");
      // Optionally trigger access to app state to redirect, or rely on App.js check
      // For now, removing the token will cause App.js to re-render Login on next check/refresh
      // To force immediate update if we are not using a context:
      if (window.location.pathname !== "/") {
          window.location.href = "/"; 
      }
    }
    return Promise.reject(error);
  }
);

export default API;

export const register = (username, password) => API.post("register/", { username, password });

export const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  // Content-Type is multipart/form-data, let browser set boundary
  return API.post("upload/", formData, {
    headers: {
        "Content-Type": "multipart/form-data",
    }
  });
};

export const getHistory = () => API.get("history/");

export const generateReport = (datasetId) =>
  API.post("generate-report/", { dataset_id: datasetId }, { responseType: "blob" });
