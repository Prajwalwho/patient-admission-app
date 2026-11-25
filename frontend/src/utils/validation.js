const NAME_RE = /^[A-Za-z]+(?: [A-Za-z]+)*$/;

// Today's date in India as YYYY-MM-DD (same rule as the backend)
export function todayISO() {
  return new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Kolkata" }).format(
    new Date()
  );
}

const SELECTS = [
  ["gender", "Gender", "genders"],
  ["ward", "Ward", "wards"],
  ["department", "Department", "departments"],
  ["doctor", "Doctor", "doctors"],
];

// Returns an object containing only the fields that have errors
export function validatePatient(values, options) {
  const errors = {};

  const name = values.name.trim();
  if (!name) errors.name = "Name is required";
  else if (name.length > 100) errors.name = "Name must be at most 100 characters";
  else if (!NAME_RE.test(name)) errors.name = "Name must contain letters only";

  const age = String(values.age).trim();
  if (age === "") errors.age = "Age is required";
  else if (!/^\d+$/.test(age) || Number(age) > 120)
    errors.age = "Age must be a whole number between 0 and 120";

  for (const [field, label, key] of SELECTS) {
    if (!values[field]) errors[field] = `${label} is required`;
    else if (!options[key]?.includes(values[field]))
      errors[field] = `Invalid ${field}`;
  }

  if (!values.admission_date) errors.admission_date = "Admission date is required";
  else if (values.admission_date > todayISO())
    errors.admission_date = "Admission date cannot be in the future";

  return errors;
}