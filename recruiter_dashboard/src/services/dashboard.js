import api from "./api";

export async function getDashboardAnalytics() {
  const response = await api.get("/jobs/analytics");

  return response.data;
}
