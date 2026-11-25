function formatDate(iso) {
  return new Date(iso + "T00:00:00").toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

export default function PatientTable({
  patients,
  loading,
  onEdit,
  onDischarge,
  onDelete,
}) {
  if (!loading && patients.length === 0) {
    return <p className="empty">No patients found.</p>;
  }

  return (
    <table className={loading ? "loading" : ""}>
      <thead>
        <tr>
          <th>Name</th>
          <th>Age</th>
          <th>Gender</th>
          <th>Ward</th>
          <th>Department</th>
          <th>Doctor</th>
          <th>Admitted</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {patients.map((p) => {
          const discharged = p.status === "Discharged";
          return (
            <tr key={p.id}>
              <td data-label="Name" className="name">{p.name}</td>
              <td data-label="Age">{p.age}</td>
              <td data-label="Gender">{p.gender}</td>
              <td data-label="Ward">{p.ward}</td>
              <td data-label="Department">{p.department}</td>
              <td data-label="Doctor">{p.doctor}</td>
              <td data-label="Admitted">{formatDate(p.admission_date)}</td>
              <td data-label="Status">
                <span className={`badge ${discharged ? "badge-off" : "badge-on"}`}>
                  {p.status}
                </span>
              </td>
              <td className="actions">
                <button className="btn btn-small" onClick={() => onEdit(p)}>
                  Edit
                </button>
                <button
                  className="btn btn-small"
                  disabled={discharged}
                  onClick={() => onDischarge(p)}
                >
                  Discharge
                </button>
                <button
                  className="btn btn-small btn-danger"
                  onClick={() => onDelete(p)}
                >
                  Delete
                </button>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}