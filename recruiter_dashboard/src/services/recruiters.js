import api from "./api";

export const getRecruiters = async () => {
  const response = await api.get("/recruiters/");
  return response.data;
};

export const createRecruiter = async (recruiter) => {
  const response = await api.post(
    "/recruiters/",
    recruiter
  );

  return response.data;
};

export const deleteRecruiter = async (id) => {
  const response = await api.delete(
    `/recruiters/${id}`
  );

  return response.data;
};