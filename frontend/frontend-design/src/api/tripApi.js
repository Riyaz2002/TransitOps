import api from "./axios";

export const getTripsApi = async () => {
  const response = await api.get("trips");
  return response.data;
};

export const createTripApi = async (payload) => {
  const response = await api.post("trips", payload);
  return response.data;
};

export const updateTripApi = async (id, payload) => {
  const response = await api.patch(`trips/${id}`, payload);
  return response.data;
};

export const dispatchTripApi = async (id) => {
  const response = await api.post(`trips/${id}/dispatch`);
  return response.data;
};

export const completeTripApi = async (id) => {
  const response = await api.post(`trips/${id}/complete`);
  return response.data;
};

export const cancelTripApi = async (id) => {
  const response = await api.post(`trips/${id}/cancel`);
  return response.data;
};
