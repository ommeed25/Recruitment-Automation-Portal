import api from "./api";

export const getRecruiters = async () => {
  const response = await api.get("/recruiters/");

  return response.data;
};