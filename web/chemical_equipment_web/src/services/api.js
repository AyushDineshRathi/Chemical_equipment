import axios from "axios";

const API = axios.create({
  baseURL: "https://chemical-equipment-ituh.onrender.com/api/",
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default API;

export const register = (username, password) => API.post("register/", { username, password });

export const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return API.post("upload/", formData);
};

export const getHistory = () => API.get("history/");

export const generateReport = (datasetId) =>
  API.post("generate-report/", { dataset_id: datasetId }, { responseType: "blob" });