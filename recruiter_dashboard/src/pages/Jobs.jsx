import { useEffect, useState } from "react";
import { getJobs } from "../services/jobs";
import JobsTable from "../components/jobs/JobsTable";
import PreviewModal from "../components/jobs/PreviewModal";
import "../styles/jobs.css";

export default function Jobs() {
  const [jobs, setJobs] = useState([]);

  const [page, setPage] = useState(1);

  const [totalPages, setTotalPages] = useState(1);

  const [error, setError] = useState("");
  const [selectedJob, setSelectedJob] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    let cancelled = false;

    const fetchJobs = async () => {
      console.log("Calling API...");

      try {
        const data = await getJobs(page);

        console.log("API Response:", data);

        if (!cancelled) {
          setJobs(data.items);
          setTotalPages(data.total_pages);
          setError("");
        }
      } catch (err) {
        console.error("API Error:", err);

        if (!cancelled) {
          setError(err.response?.data?.detail || err.message);
        }
      }
    };

    void fetchJobs();

    return () => {
      cancelled = true;
    };
  }, [page]);

  if (error) {
    return <h1>Error: {error}</h1>;
  }


  function handlePublish(jobId) {
    setJobs((previousJobs) =>
      previousJobs.map((job) =>
        job.job_id === jobId
          ? {
              ...job,
              linkedin_posted: true,
            }
          : job
      )
    );
  }

  function handlePreview(job) {
    setSelectedJob(job);
    setIsModalOpen(true);
  }

  function handleClose() {
    setIsModalOpen(false);
    setSelectedJob(null);
  }

  return (
    <div>
      <h1>Jobs</h1>

      <JobsTable jobs={jobs} onPublish={handlePublish} onPreview={handlePreview} />

      <PreviewModal open={isModalOpen} job={selectedJob} onClose={handleClose} />

      <div className="pagination">
        <button disabled={page === 1} onClick={() => setPage(page - 1)}>
          Previous
        </button>

        <span>
          Page {page} of {totalPages}
        </span>

        <button
          disabled={page === totalPages}
          onClick={() => setPage(page + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
}

