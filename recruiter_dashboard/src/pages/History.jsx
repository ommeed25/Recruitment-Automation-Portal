import { useEffect, useState } from "react";
import { getHistory } from "../services/history";

export default function History() {
  const [history, setHistory] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState("");

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await getHistory(page, 10, search);

        setHistory(data.items);
        setTotalPages(data.total_pages);
      } catch (err) {
        console.error(err);
      }
    };

    void loadHistory();
  }, [page,search]);

  return (
    <div>
      <h1>LinkedIn Posting History</h1>

      <div className="history-toolbar">
        <input
          className="history-search"
          type="text"
          placeholder="Search Job Title..."
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
        />
      </div>

      <table className="jobs-table">
        <thead>
          <tr>
            <th>Job ID</th>
            <th>Title</th>
            <th>Recruiter</th>
            <th>Status</th>
            <th>Posted At</th>
          </tr>
        </thead>

        <tbody>
          {history.map((post, index) => (
            <tr key={index}>
              <td>{post.job_id}</td>
              <td>{post.title}</td>
              <td>{post.recruiter}</td>
              <td>{post.status}</td>
              <td>{new Date(post.posted_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
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
