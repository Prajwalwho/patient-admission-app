import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
});

export const getOptions = () => api.get("/options").then((r) => r.data);
export const getPatients = (params) =>
  api.get("/patients", { params }).then((r) => r.data);
export const createPatient = (data) =>
  api.post("/patients", data).then((r) => r.data);
export const updatePatient = (id, data) =>
  api.put(`/patients/${id}`, data).then((r) => r.data);
export const deletePatient = (id) => api.delete(`/patients/${id}`);
export const dischargePatient = (id) =>
  api.patch(`/patients/${id}/discharge`).then((r) => r.data);

// Turns a backend error into { fieldErrors, message }
export function extractErrors(err) {
  const data = err.response?.data;
  if (data?.errors) {
    return { fieldErrors: data.errors, message: data.message };
  }
  return {
    fieldErrors: {},
    message: data?.message || "Cannot reach the server. Please try again.",
  };
}