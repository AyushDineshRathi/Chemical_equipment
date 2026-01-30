function Card({ title, children }) {
  return (
    <div style={{
      background: "var(--card)",
      borderRadius: "12px",
      padding: "20px",
      marginBottom: "20px",
      boxShadow: "0 8px 24px rgba(0,0,0,0.06)"
    }}>
      {title && <h3 style={{ marginBottom: "16px" }}>{title}</h3>}
      {children}
    </div>
  );
}

export default Card;
