import api from "./api";

export async function publishJob(jobId) {
  const response = await api.post(`/auth/linkedin/publish/${jobId}`);

  return response.data;
}