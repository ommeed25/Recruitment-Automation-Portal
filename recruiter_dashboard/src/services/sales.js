import api from "./api";

export const getSalesSettings = async () => {
  const response = await api.get("/sales/settings/");
  return response.data;
};

export const updateSalesSettings = async (isEnabled, postingTime) => {
  const response = await api.put("/sales/settings/", null, {
    params: {
      is_enabled: isEnabled,
      posting_time: postingTime,
    },
  });
  return response.data;
};

export const getSalesImages = async () => {
  const response = await api.get("/sales/images/");
  return response.data;
};

export const uploadSalesImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/sales/images/upload", formData);
  return response.data;
};

export const selectSalesImage = async (imageId) => {
  const response = await api.post(`/sales/images/${imageId}/select`);
  return response.data;
};

export const deleteSalesImage = async (imageId) => {
  const response = await api.delete(`/sales/images/${imageId}`);
  return response.data;
};

export const getSalesHashtags = async () => {
  const response = await api.get("/sales/hashtags/");
  return response.data;
};

export const addSalesHashtags = async (hashtags) => {
  const response = await api.post("/sales/hashtags/bulk", {
    hashtags,
  });
  return response.data;
};

export const deleteSalesHashtag = async (hashtagId) => {
  const response = await api.delete(`/sales/hashtags/${hashtagId}`);
  return response.data;
};

export const getSalesAccounts = async () => {
  const response = await api.get("/sales/accounts/");
  return response.data;
};

export const createSalesAccount = async (data) => {
  const response = await api.post("/sales/accounts/", data);
  return response.data;
};

export const deleteSalesAccount = async (accountId) => {
  const response = await api.delete(`/sales/accounts/${accountId}`);
  return response.data;
};