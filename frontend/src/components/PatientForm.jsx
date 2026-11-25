import { useState } from "react";
import { createPatient, updatePatient, extractErrors } from "../api/client";
import { validatePatient, todayISO } from "../utils/validation";

const BLANK = {
  name: "",
  age: "",
  gender: "",
  ward: "",
  department: "",
  doctor: "",
  admission_date: "",
};

export default function PatientForm({ patient, options, onClose, onSaved }) {
  const isEdit = Boolean(patient);
  const [values, setValues] = useState(
    isEdit ? { ...patient, age: String(patient.age) } : BLANK
  );
  const [errors, setErrors] = useState({});
  const [serverMessage, setServerMessage] = useState("");
  const [saving, setSaving] = useState(false);

  const change = (e) => {
    const { name, value } = e.target;
    setValues((v) => ({ ...v, [name]: value }));
    if (errors[name]) setErrors((er) => ({ ...er, [name]: undefined }));
  };

  const submit = async (e) => {
    e.preventDefault();
    setServerMessage("");
    const found = validatePatient(values, options);
    setErrors(found);
    if (Object.keys(found).length > 0) return;

    const payload = {
      name: values.name.trim(),
      age: Number(values.age),
      gender: values.gender,
      ward: values.ward,
      department: values.department,
      doctor: values.doctor,
      admission_date: values.admission_date,
    };

    setSaving(true);
    try {
      const saved = isEdit
        ? await updatePatient(patient.id, payload)
        : await createPatient(payload);
      onSaved(saved, isEdit);
    } catch (err) {
      const { fieldErrors, message } = extractErrors(err);
      setErrors(fieldErrors);
      setServerMessage(
        Object.keys(fieldErrors).length ? "Please fix the highlighted fields." : message
      );
    } finally {
      setSaving(false);
    }
  };

  const select = (name, label, list) => (
    <div className={`field ${errors[name] ? "has-error" : ""}`}>
      <label htmlFor={name}>{label}</label>
      <select id={name} name={name} value={values[name]} onChange={change}>
        <option value="">Select {label.toLowerCase()}</option>
        {list.map((item) => (
          <option key={item} value={item}>
            {item}
          </option>
        ))}
      </select>
      {errors[name] && <span className="error">{errors[name]}</span>}
    </div>
  );

  return (
    <div className="overlay" role="dialog" aria-modal="true">
      <form className="modal" onSubmit={submit} noValidate>
        <h2>{isEdit ? "Edit patient" : "Add patient"}</h2>
        {serverMessage && <div className="alert">{serverMessage}</div>}

        <div className="form-grid">
          <div className={`field ${errors.name ? "has-error" : ""}`}>
            <label htmlFor="name">Name</label>
            <input
              id="name"
              name="name"
              value={values.name}
              onChange={change}
              placeholder="e.g. Ravi Kumar"
            />
            {errors.name && <span className="error">{errors.name}</span>}
          </div>

          <div className={`field ${errors.age ? "has-error" : ""}`}>
            <label htmlFor="age">Age</label>
            <input
              id="age"
              name="age"
              type="number"
              min="0"
              max="120"
              value={values.age}
              onChange={change}
              placeholder="0 - 120"
            />
            {errors.age && <span className="error">{errors.age}</span>}
          </div>

          {select("gender", "Gender", options.genders)}
          {select("ward", "Ward", options.wards)}
          {select("department", "Department", options.departments)}
          {select("doctor", "Doctor", options.doctors)}

          <div className={`field ${errors.admission_date ? "has-error" : ""}`}>
            <label htmlFor="admission_date">Admission date</label>
            <input
              id="admission_date"
              name="admission_date"
              type="date"
              max={todayISO()}
              value={values.admission_date}
              onChange={change}
            />
            {errors.admission_date && (
              <span className="error">{errors.admission_date}</span>
            )}
          </div>
        </div>

        <div className="modal-actions">
          <button type="button" className="btn btn-ghost" onClick={onClose} disabled={saving}>
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? "Saving..." : isEdit ? "Save changes" : "Add patient"}
          </button>
        </div>
      </form>
    </div>
  );
}