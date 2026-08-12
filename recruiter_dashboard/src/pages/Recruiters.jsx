import { useEffect, useState } from "react";
import "./Recruiters.css";
import {
  getRecruiters,
  createRecruiter,
  deleteRecruiter,
} from "../services/recruiters";

export default function Recruiters() {
  const [recruiters, setRecruiters] = useState([]);

  const [showModal, setShowModal] = useState(false);

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [employeeId, setEmployeeId] = useState("");

  const loadRecruiters = async () => {
    try {
      const data = await getRecruiters();
      setRecruiters(data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    let isMounted = true;

    const fetchRecruiters = async () => {
      await loadRecruiters();
      if (!isMounted) return;
    };

    void fetchRecruiters();

    return () => {
      isMounted = false;
    };
  }, []);

  const handleCreate = async () => {
    try {
      await createRecruiter({
        full_name: fullName,
        email,
        employee_id: employeeId || null,
      });

      setFullName("");
      setEmail("");
      setEmployeeId("");

      setShowModal(false);

      loadRecruiters();
    } catch (error) {
      alert(error.response?.data?.detail || "Unable to create recruiter");
    }
  };

  const handleDelete = async (id, recruiter) => {
    if (
      !window.confirm(
        `Delete ${recruiter.full_name}?\n\nThis will remove the recruiter and any related LinkedIn post history.`,
      )
    ) {
      return;
    }

    try {
      await deleteRecruiter(id);

      loadRecruiters();
    } catch (error) {
      alert(error.response?.data?.detail || "Unable to delete recruiter");
    }
  };

  return (
    <div>
      <div className="recruiters-header">
        <h1>Recruiters</h1>

        <button className="add-btn" onClick={() => setShowModal(true)}>
          + Add Recruiter
        </button>
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Add Recruiter</h3>

            <input
              placeholder="Full Name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />

            <input
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              placeholder="Employee ID (Optional)"
              value={employeeId}
              onChange={(e) => setEmployeeId(e.target.value)}
            />

            <div className="modal-actions">
              <button className="cancel-btn" onClick={() => setShowModal(false)}>
                Cancel
              </button>
              <button className="save-btn" onClick={handleCreate}>
                Save
              </button>
            </div>
          </div>
        </div>
      )}

      <table className="jobs-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>LinkedIn</th>
            <th>Delete</th>
          </tr>
        </thead>

        <tbody>
          {recruiters.map((recruiter) => (
            <tr key={recruiter.id}>
              <td>{recruiter.full_name}</td>

              <td>{recruiter.email}</td>

              <td>
                {recruiter.connected ? "🟢 Connected" : "🔴 Not Connected"}
              </td>

              <td>
                {recruiter.connected ? (
                  <button className="connected-btn" disabled>
                    Connected
                  </button>
                ) : (
                  <button
                    className="connect-btn"
                    onClick={() => {
                      window.location.href = `/api/auth/linkedin/authorize?email=${encodeURIComponent(
                            recruiter.email,
                       )}`;
                    }}
                  >
                    Connect
                  </button>
                )}
              </td>

              <td>
                  <button
 			 className="delete-btn"
 			 disabled={!recruiter.id}
 			 onClick={() => handleDelete(recruiter.id, recruiter)}
			>
 			 🗑 Delete
		</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
