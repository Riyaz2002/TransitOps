import api from "./axios";

export const getVehiclesApi = async () => {
  const response = await api.get("/vehicles/");
  return response.data;
};

export const createVehicleApi = async (payload) => {
  const response = await api.post("/vehicles/", payload);
  return response.data;
};

export const updateVehicleApi = async (id, payload) => {
  const response = await api.put(`/vehicles/${id}/`, payload);
  return response.data;
};

export const deleteVehicleApi = async (id) => {
  await api.delete(`/vehicles/${id}/`);
};
