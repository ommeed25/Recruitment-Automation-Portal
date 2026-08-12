import api from "./api";

export async function getVendorSettings() {
  const response = await api.get("/vendor/settings");
  return response.data;
}

export async function getVendorImages() {
  const response = await api.get("/vendor/images");
  return response.data;
}

export async function getVendorHashtags() {
  const response = await api.get("/vendor/hashtags");
  return response.data;
}

export async function selectVendorImage(imageId) {
  const response = await api.post(`/vendor/images/${imageId}/select`);

  return response.data;
}

export async function uploadVendorImage(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/vendor/images/upload",
    formData
  );

  return response.data;
}

export async function deleteVendorImage(imageId) {
  const response = await api.delete(
    `/vendor/images/${imageId}`
  );

  return response.data;
}

export async function addVendorHashtag(hashtag) {
  const response = await api.post("/vendor/hashtags", {
    hashtag,
  });

  return response.data;
}

export async function addVendorHashtags(hashtags) {
  const response = await api.post(
    "/vendor/hashtags/bulk",
    {
      hashtags,
    }
  );

  return response.data;
}

export async function deleteVendorHashtag(hashtagId) {
  const response = await api.delete(
    `/vendor/hashtags/${hashtagId}`
  );

  return response.data;
}

export async function updateVendorSettings(isEnabled, postingTime) {
  const response = await api.put("/vendor/settings", null, {
    params: {
      is_enabled: isEnabled,
      posting_time: postingTime,
    },
  });

  return response.data;
}