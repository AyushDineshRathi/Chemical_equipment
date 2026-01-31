import Card from "./Card";

export default function KPI({ label, value, unit }) {
  return (
    <Card style={{ 
      marginBottom: 0, 
      display: "flex", 
      flexDirection: "column", 
      justifyContent: "center",
      alignItems: "center",
      textAlign: "center" 
    }}>
      <div style={{ 
        fontSize: "14px", 
        color: "var(--text-light)", 
        fontWeight: "500", 
        marginBottom: "8px", 
        textTransform: "uppercase",
        letterSpacing: "0.5px"
      }}>
        {label}
      </div>
      <div style={{ 
        fontSize: "32px", 
        fontWeight: "700", 
        color: "var(--primary)",
        lineHeight: 1 
      }}>
        {value} <span style={{ fontSize: "16px", color: "var(--text-light)", fontWeight: "400" }}>{unit}</span>
      </div>
    </Card>
  );
}