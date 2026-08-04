import { useEffect, useState } from "react";
import { getRecruiters } from "../services/recruiters";

export default function Recruiters() {
  const [recruiters, setRecruiters] = useState([]);

  useEffect(() => {
    const loadRecruiters = async () => {
      try {
        const data = await getRecruiters();
        setRecruiters(data);
      } catch (error) {
        console.error(error);
      }
    };

    void loadRecruiters();
  }, []);

  return (
    <div>
      <h1>Recruiters</h1>

      <table className="jobs-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {recruiters.map((recruiter, index) => (
            <tr key={index}>
              <td>{recruiter.full_name}</td>

              <td>{recruiter.email}</td>

              <td>
                {recruiter.connected ? "🟢 Connected" : "🔴 Not Connected"}
              </td>

              <td>
                {recruiter.connected ? (
                  <button disabled>Connected</button>
                ) : (
                  <button
                    onClick={() => {
                      window.location.href = `http://127.0.0.1:8000/auth/linkedin/authorize?email=${encodeURIComponent(
                        recruiter.email,
                      )}`;
                    }}
                  >
                    Connect LinkedIn
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
