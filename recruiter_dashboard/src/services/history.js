import axios from "axios";

const API = "http://127.0.0.1:8000";

export async function getHistory(page = 1, size = 10, search = "") {
  const response = await axios.get(`${API}/history`, {
    params: {
      page,
      size,
      search,
    },
  });

  return response.data;
}
