import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

export const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return API.post("upload/", formData);
};

export const getSummary = (id) => API.get(`summary/${id}/`);
export const getHistory = () => API.get("history/");
