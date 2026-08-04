import { Briefcase, CheckCircle, Clock3, XCircle, Users } from "lucide-react";

import StatCard from "../components/dashboard/StatCard";
import ChartCard from "../components/dashboard/ChartCard";
import StatusCard from "../components/dashboard/StatusCard";
import { useEffect, useState } from "react";
import { getDashboardAnalytics } from "../services/dashboard";

import "../styles/dashboard.css";

export default function Dashboard() {
  const [analytics, setAnalytics] = useState({
    total_jobs: 0,
    published_jobs: 0,
    pending_jobs: 0,
    failed_jobs: 0,
    recruiters: 0,
  });

  useEffect(() => {
    let cancelled = false;

    const loadAnalytics = async () => {
      try {
        const data = await getDashboardAnalytics();

        if (!cancelled) {
          setAnalytics({
            total_jobs: data.total_jobs ?? 0,
            published_jobs: data.published_jobs ?? 0,
            pending_jobs: data.pending_jobs ?? 0,
            failed_jobs:
              data.failed_jobs ??
              Math.max((data.total_jobs ?? 0) - (data.published_jobs ?? 0) - (data.pending_jobs ?? 0), 0),
            recruiters: data.recruiters ?? 0,
          });
        }
      } catch (error) {
        console.error(error);
      }
    };

    void loadAnalytics();

    return () => {
      cancelled = true;
    };
  }, []);

  const failedJobs = Math.max(
    analytics.failed_jobs ?? 0,
    analytics.total_jobs - analytics.published_jobs - analytics.pending_jobs
  );

  return (
    <div className="dashboard-page">
      <div className="card-grid">
        <StatCard
          title="Total Jobs"
          value={analytics.total_jobs}
          icon={<Briefcase />}
          color="#2563eb"
        />

        <StatCard
          title="Published"
          value={analytics.published_jobs}
          icon={<CheckCircle />}
          color="#16a34a"
        />

        <StatCard
          title="Pending"
          value={analytics.pending_jobs}
          icon={<Clock3 />}
          color="#eab308"
        />

        <StatCard title="Failed" value={failedJobs} icon={<XCircle />} color="#dc2626" />

        <StatCard
          title="Recruiters"
          value={analytics.recruiters}
          icon={<Users />}
          color="#7c3aed"
        />
      </div>

      <div className="dashboard-body">
        <ChartCard />
        <StatusCard published={analytics.published_jobs} pending={analytics.pending_jobs} failed={failedJobs} />
      </div>
    </div>
  );
}
