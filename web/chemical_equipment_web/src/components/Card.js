function Card({ title, children, style }) {
  return (
    <div style={{
      background: "var(--card)",
      borderRadius: "var(--radius)",
      padding: "24px",
      marginBottom: "24px",
      boxShadow: "var(--shadow-sm)",
      border: "1px solid var(--border)",
      ...style
    }}>
      {title && (
        <h3 style={{ 
          marginBottom: "20px", 
          fontSize: "18px", 
          color: "var(--text)",
          borderBottom: "1px solid var(--border)",
          paddingBottom: "12px"
        }}>
          {title}
        </h3>
      )}
      {children}
    </div>
  );
}

export default Card;
