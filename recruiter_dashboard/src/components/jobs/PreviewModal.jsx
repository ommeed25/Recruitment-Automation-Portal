import { useEffect, useState } from "react";
import "../../styles/preview-modal.css";

function parseSkills(value) {
  if (Array.isArray(value)) {
    return value.join(", ");
  }

  if (typeof value === "string") {
    return value;
  }

  return "";
}

function createInitialFormState(job) {
  return {
    title: job?.job_posting_title || "",
    location: job?.job_work_location || "",
    experience: job?.experience_slab || "",
    employmentType: job?.employment_type || "",
    jobMode: job?.job_mode || "",
    noticePeriod: job?.notice_period || "",
    skills: parseSkills(job?.job_posting_skills || job?.skills || ""),
  };
}

function buildLinkedInPreview(values) {
  const skills = values.skills
    .split(/[,\n]/)
    .map((skill) => skill.trim())
    .filter(Boolean);

  const lines = [
    `🚀 We're Hiring | ${values.title || "Job Opportunity"}`,
    "",
    values.location ? `📍 Location: ${values.location}` : "",
    values.experience ? `💼 Experience: ${values.experience}` : "",
    values.employmentType ? `🏢 Employment Type: ${values.employmentType}` : "",
    values.jobMode ? `🖥 Mode: ${values.jobMode}` : "",
    values.noticePeriod ? `📌 Notice Period: ${values.noticePeriod}` : "",
    skills.length ? "\n🛠 Skills:" : "",
    ...skills.map((skill) => `- ${skill}`),
    "",
    "#Hiring #Jobs #UnionSys",
  ];

  return lines.filter(Boolean).join("\n");
}

export default function PreviewModal({ open, job, onClose }) {
  const [formValues, setFormValues] = useState(createInitialFormState(job));

  useEffect(() => {
    if (open) {
      setFormValues(createInitialFormState(job));
    }
  }, [open, job]);

  if (!open) {
    return null;
  }

  const handleChange = (field) => (event) => {
    setFormValues((previous) => ({
      ...previous,
      [field]: event.target.value,
    }));
  };

  const handleSave = () => {
    console.log("updatedJob", {
      ...job,
      job_posting_title: formValues.title,
      job_work_location: formValues.location,
      experience_slab: formValues.experience,
      employment_type: formValues.employmentType,
      job_mode: formValues.jobMode,
      notice_period: formValues.noticePeriod,
      skills: formValues.skills,
    });
  };

  const handlePublish = () => {
    console.log("Publish clicked");
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(event) => event.stopPropagation()}>
        <div className="modal-header">
          <div>
            <p className="modal-kicker">Recruiter workflow</p>
            <h2>Preview Job</h2>
          </div>
          <button type="button" className="icon-button" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="modal-body">
          <div className="modal-form">
            <label>
              <span>Title</span>
              <input value={formValues.title} onChange={handleChange("title")} />
            </label>

            <label>
              <span>Location</span>
              <input value={formValues.location} onChange={handleChange("location")} />
            </label>

            <label>
              <span>Experience</span>
              <input value={formValues.experience} onChange={handleChange("experience")} />
            </label>

            <label>
              <span>Employment Type</span>
              <input value={formValues.employmentType} onChange={handleChange("employmentType")} />
            </label>

            <label>
              <span>Job Mode</span>
              <input value={formValues.jobMode} onChange={handleChange("jobMode")} />
            </label>

            <label>
              <span>Notice Period</span>
              <input value={formValues.noticePeriod} onChange={handleChange("noticePeriod")} />
            </label>

            <label>
              <span>Skills</span>
              <textarea rows="4" value={formValues.skills} onChange={handleChange("skills")} />
            </label>
          </div>

          <div className="modal-preview-panel">
            <h3>LinkedIn Preview</h3>
            <pre>{buildLinkedInPreview(formValues)}</pre>
          </div>
        </div>

        <div className="modal-actions">
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancel
          </button>
          <button type="button" className="btn btn-primary" onClick={handleSave}>
            Save Changes
          </button>
          <button type="button" className="btn btn-accent" onClick={handlePublish}>
            Publish
          </button>
        </div>
      </div>
    </div>
  );
}
