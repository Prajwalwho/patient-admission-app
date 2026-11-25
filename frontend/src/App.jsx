import { useEffect, useState } from "react";
import {
  getOptions,
  getPatients,
  deletePatient,
  dischargePatient,
  extractErrors,
} from "./api/client";
import Filters from "./components/Filters";
import PatientTable from "./components/PatientTable";
import PatientForm from "./components/PatientForm";
import ConfirmDialog from "./components/ConfirmDialog";

const EMPTY_FILTERS = { ward: "", department: "", doctor: "" };

export default function App() {
  const [options, setOptions] = useState({
    genders: [],
    wards: [],
    departments: [],
    doctors: [],
  });
  const [patients, setPatients] = useState([]);
  const [filters, setFilters] = useState(EMPTY_FILTERS);
  const [searchInput, setSearchInput] = useState("");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [reloadKey, setReloadKey] = useState(0);

  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [deleting, setDeleting] = useState(null);
  const [busy, setBusy] = useState(false);
  const [toast, setToast] = useState(null);

  // Load dropdown options once
  useEffect(() => {
    getOptions()
      .then(setOptions)
      .catch((e) => setError(extractErrors(e).message));
  }, []);

  // Debounce the search box (300 ms)
  useEffect(() => {
    const t = setTimeout(() => setSearch(searchInput), 300);
    return () => clearTimeout(t);
  }, [searchInput]);

  // Load patients whenever filters, search or reloadKey change
  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getPatients({ ...filters, search })
      .then((data) => {
        if (cancelled) return;
        setPatients(data);
        setError("");
      })
      .catch((e) => {
        if (!cancelled) setError(extractErrors(e).message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [filters, search, reloadKey]);

  // Auto-hide toast
  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(null), 3000);
    return () => clearTimeout(t);
  }, [toast]);

  const reload = () => setReloadKey((k) => k + 1);
  const notify = (text, type = "success") => setToast({ text, type });

  const openAdd = () => {
    setEditing(null);
    setFormOpen(true);
  };
  const openEdit = (patient) => {
    setEditing(patient);
    setFormOpen(true);
  };

  const handleSaved = (_saved, wasEdit) => {
    setFormOpen(false);
    setEditing(null);
    notify(wasEdit ? "Patient updated" : "Patient added");
    reload();
  };

  const handleDischarge = async (patient) => {
    try {
      await dischargePatient(patient.id);
      notify(`${patient.name} marked as discharged`);
      reload();
    } catch (e) {
      notify(extractErrors(e).message, "error");
    }
  };

  const handleDelete = async () => {
    setBusy(true);
    try {
      await deletePatient(deleting.id);
      notify("Patient deleted");
      setDeleting(null);
      reload();
    } catch (e) {
      notify(extractErrors(e).message, "error");
      setDeleting(null);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="app">
      <header className="topbar">
        <div>
          <h1>Patient Admission Management</h1>
          <p className="subtitle">{patients.length} patient(s) shown</p>
        </div>
        <button className="btn btn-primary" onClick={openAdd}>
          + Add patient
        </button>
      </header>

      <main>
        <Filters
          options={options}
          filters={filters}
          onFilterChange={(key, value) =>
            setFilters((f) => ({ ...f, [key]: value }))
          }
          searchInput={searchInput}
          onSearchChange={setSearchInput}
          onClear={() => {
            setFilters(EMPTY_FILTERS);
            setSearchInput("");
            setSearch("");
          }}
        />

        {error && <div className="alert">{error}</div>}
        {loading && patients.length === 0 && !error && (
          <p className="empty">Loading patients...</p>
        )}

        <PatientTable
          patients={patients}
          loading={loading}
          onEdit={openEdit}
          onDischarge={handleDischarge}
          onDelete={setDeleting}
        />
      </main>

      {formOpen && (
        <PatientForm
          patient={editing}
          options={options}
          onClose={() => setFormOpen(false)}
          onSaved={handleSaved}
        />
      )}

      {deleting && (
        <ConfirmDialog
          title="Delete patient?"
          message={`Are you sure you want to delete ${deleting.name}? This cannot be undone.`}
          confirmLabel="Delete"
          busy={busy}
          onConfirm={handleDelete}
          onCancel={() => setDeleting(null)}
        />
      )}

      {toast && <div className={`toast toast-${toast.type}`}>{toast.text}</div>}
    </div>
  );
}