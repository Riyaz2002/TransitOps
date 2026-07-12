import api from "./axios";

export const getDriversApi = async () => {
  const response = await api.get("drivers");
  return response.data;
};

export const createDriverApi = async (payload) => {
  const response = await api.post("drivers", payload);
  return response.data;
};

export const updateDriverApi = async (id, payload) => {
  const response = await api.patch(`drivers/${id}`, payload);
  return response.data;
};
