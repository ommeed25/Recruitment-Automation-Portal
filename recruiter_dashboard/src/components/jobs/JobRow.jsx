import { publishJob } from "../../services/linkedin";

export default function JobRow({ job, onPublish, onPreview }) {
  return (
    <tr>
      <td>{job.job_id}</td>

      <td>{job.job_posting_title}</td>

      <td>{job.job_work_location}</td>

      <td>{job.experience_slab}</td>

      <td>{job.linkedin_posted ? "Published" : "Pending"}</td>

      <td>
        <button className="preview-btn" onClick={() => onPreview(job)}>
          Preview
        </button>

        <button
          disabled={job.linkedin_posted}
          onClick={async () => {
            try {
              await publishJob(job.job_id);

              onPublish(job.job_id);

              alert("Job published successfully.");
            } catch (error) {
              console.error(error);

              alert("Publishing failed.");
            }
          }}
        >
          {job.linkedin_posted ? "Published" : "Publish"}
        </button>
      </td>
    </tr>
  );
}
