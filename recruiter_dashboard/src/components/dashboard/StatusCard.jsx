import "../../styles/cards.css";

export default function StatusCard({ published = 0, pending = 0, failed = 0 }) {
  const data = [
    { title: "Published", value: published, color: "#16a34a" },
    { title: "Pending", value: pending, color: "#eab308" },
    { title: "Failed", value: failed, color: "#dc2626" },
  ];

  return (
    <div className="status-card">
      <h2>Publish Status</h2>

      {data.map((item) => (
        <div className="status-row" key={item.title}>
          <span>{item.title}</span>

          <span
            style={{
              color: item.color,
              fontWeight: 700,
            }}
          >
            {item.value}
          </span>
        </div>
      ))}
    </div>
  );
}
