import axios from "axios";

const API = "/api";

export async function login(email, password) {
  const response = await axios.post(`${API}/auth/login`, {
    email,
    password,
  });

  return response.data;
}
