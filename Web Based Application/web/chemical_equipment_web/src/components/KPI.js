import Card from "./Card";

export default function KPI({ label, value, unit }) {
  return (
    <Card>
      <div style={{ fontSize: "14px", color: "var(--secondary)" }}>
        {label}
      </div>
      <div style={{ fontSize: "28px", fontWeight: "600" }}>
        {value} {unit}
      </div>
    </Card>
  );
}