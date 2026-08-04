import JobRow from "./JobRow";

import "../../styles/jobs.css";

export default function JobsTable({ jobs, onPublish, onPreview }) {
  return (
    <table className="jobs-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Job Title</th>
          <th>Location</th>
          <th>Experience</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        {jobs.map((job) => (
          <JobRow key={job.job_id} job={job} onPublish={onPublish} onPreview={onPreview} />
        ))}
      </tbody>
    </table>
  );
}
