import axios from "axios";

const API = "http://127.0.0.1:8000";

export async function login(email, password) {
  const response = await axios.post(`${API}/auth/login`, {
    email,
    password,
  });

  return response.data;
}