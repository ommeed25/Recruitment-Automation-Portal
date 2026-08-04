import { NavLink, Outlet } from "react-router-dom";
import {
  LayoutDashboard,
  BriefcaseBusiness,
  Users,
  History,
  Settings,
} from "lucide-react";

import "../styles/layout.css";
import "../styles/sidebar.css";

const menu = [
  {
    title: "Dashboard",
    path: "/",
    icon: <LayoutDashboard size={20} />,
  },
  {
    title: "Jobs",
    path: "/jobs",
    icon: <BriefcaseBusiness size={20} />,
  },
  {
    title: "Recruiters",
    path: "/recruiters",
    icon: <Users size={20} />,
  },
  {
    title: "History",
    path: "/history",
    icon: <History size={20} />,
  },
  {
    title: "Settings",
    path: "/settings",
    icon: <Settings size={20} />,
  },
];

export default function MainLayout() {
  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="logo">RecruitAI</div>

        <nav>
          {menu.map((item) => (
            <NavLink
              key={item.title}
              to={item.path}
              className={({ isActive }) => (isActive ? "menu active" : "menu")}
            >
              {item.icon}
              <span>{item.title}</span>
            </NavLink>
          ))}
        </nav>
      </aside>

      <section className="content">
        <div className="topbar">
          <div>
            <h1>Recruitment Automation Portal</h1>

            <p>Automated LinkedIn Job Posting System</p>
          </div>

          <div className="status">
            <span className="oracle">🟢 Oracle Connected</span>

            <span className="linkedin">🟢 LinkedIn Connected</span>
          </div>
        </div>

        <Outlet />
      </section>
    </div>
  );
}
