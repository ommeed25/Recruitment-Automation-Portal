import api from "./api";

export async function getJobs(page = 1, pageSize = 10) {

    const response = await api.get("/jobs", {
        params: {
            page,
            page_size: pageSize,
        },
    });

    return response.data;
}