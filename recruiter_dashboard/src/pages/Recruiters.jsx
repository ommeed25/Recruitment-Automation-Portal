import { useCallback, useEffect, useState } from "react";
import "./Recruiters.css";

import {
  getRecruiters,
  createRecruiter,
  deleteRecruiter,
} from "../services/recruiters";

import {
  getSalesAccounts,
  createSalesAccount,
  deleteSalesAccount,
} from "../services/sales";

export default function Recruiters() {
  const [mode, setMode] = useState("vendor");

  const [accounts, setAccounts] = useState([]);

  const [showModal, setShowModal] = useState(false);

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [employeeId, setEmployeeId] = useState("");

  const isSales = mode === "sales";

  const loadAccounts = useCallback(async () => {
    try {
      const data = isSales ? await getSalesAccounts() : await getRecruiters();

      setAccounts(data);
    } catch (error) {
      console.error(error);
    }
  }, [isSales]);

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      try {
        const data = isSales ? await getSalesAccounts() : await getRecruiters();

        if (!cancelled) {
          setAccounts(data);
        }
      } catch (error) {
        if (!cancelled) {
          console.error(error);
        }
      }
    };

    void load();

    return () => {
      cancelled = true;
    };
  }, [isSales]);

  const handleModeChange = (newMode) => {
    setMode(newMode);

    setFullName("");
    setEmail("");
    setEmployeeId("");
    setShowModal(false);
    setAccounts([]);
  };

  const handleCreate = async () => {
    try {
      const payload = {
        full_name: fullName,
        email,
        employee_id: employeeId ? Number(employeeId) : null,
      };

      if (isSales) {
        await createSalesAccount(payload);
      } else {
        await createRecruiter(payload);
      }

      setFullName("");
      setEmail("");
      setEmployeeId("");
      setShowModal(false);

      await loadAccounts();
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          `Unable to create ${isSales ? "Sales account" : "recruiter"}`,
      );
    }
  };

  const handleDelete = async (id, account) => {
    if (
      !window.confirm(
        `Delete ${account.full_name}?\n\nThis will remove the ${
          isSales ? "Sales account" : "recruiter"
        } and related LinkedIn post history.`,
      )
    ) {
      return;
    }

    try {
      if (isSales) {
        await deleteSalesAccount(id);
      } else {
        await deleteRecruiter(id);
      }

      await loadAccounts();
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          `Unable to delete ${isSales ? "Sales account" : "recruiter"}`,
      );
    }
  };

  const handleConnect = (account) => {
    const endpoint = isSales
      ? "/api/sales/auth/linkedin/authorize"
      : "/api/auth/linkedin/authorize";

    const url = `${endpoint}?email=${encodeURIComponent(account.email)}`;

    window.location.assign(url);
  };

  return (
    <div>
      <div className="recruiters-header">
        <h1>Recruiters</h1>

        <button className="add-btn" onClick={() => setShowModal(true)}>
          + Add {isSales ? "Sales" : "Recruiter"}
        </button>
      </div>

      <div className="account-mode-toggle">
        <button
          type="button"
          className={!isSales ? "mode-btn active" : "mode-btn"}
          onClick={() => handleModeChange("vendor")}
        >
          Vendor
        </button>

        <button
          type="button"
          className={isSales ? "mode-btn active" : "mode-btn"}
          onClick={() => handleModeChange("sales")}
        >
          Sales
        </button>
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Add {isSales ? "Sales Account" : "Vendor Account"}</h3>

            <input
              placeholder="Full Name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />

            <input
              placeholder="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              placeholder="Employee ID (Optional)"
              value={employeeId}
              onChange={(e) => setEmployeeId(e.target.value)}
            />

            <div className="modal-actions">
              <button
                type="button"
                className="cancel-btn"
                onClick={() => setShowModal(false)}
              >
                Cancel
              </button>

              <button type="button" className="save-btn" onClick={handleCreate}>
                Add {isSales ? "Sales" : "Vendor"}
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
          {accounts.map((account) => (
            <tr key={account.id}>
              <td>{account.full_name}</td>

              <td>{account.email}</td>

              <td>{account.connected ? "🟢 Connected" : "🔴 Not Connected"}</td>

              <td>
                {account.connected ? (
                  <button type="button" className="connected-btn" disabled>
                    Connected
                  </button>
                ) : (
                  <button
                    type="button"
                    className="connect-btn"
                    onClick={() => handleConnect(account)}
                  >
                    Connect
                  </button>
                )}
              </td>

              <td>
                <button
                  type="button"
                  className="delete-btn"
                  disabled={!account.id}
                  onClick={() => handleDelete(account.id, account)}
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
