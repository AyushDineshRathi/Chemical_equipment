import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default API;

export const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return API.post("upload/", formData);
};

export const getHistory = () => API.get("history/");