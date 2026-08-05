import api from "./api";

export async function getDashboardAnalytics() {
  const response = await api.get("/jobs/analytics");

  return response.data;
}

export async function getWeeklyJobStats() {
  const response = await api.get("/jobs/analytics/weekly");

  return response.data;
}
