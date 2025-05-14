function InfoCard({ title, children }) {
    return (
        <div className="info-card">
            <h3>{title}</h3>
            <p>{children}</p>
        </div>
    );
}

export default InfoCard;