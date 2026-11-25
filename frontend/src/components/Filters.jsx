export default function Filters({
  options,
  filters,
  onFilterChange,
  searchInput,
  onSearchChange,
  onClear,
}) {
  const selects = [
    ["ward", "Ward", options.wards],
    ["department", "Department", options.departments],
    ["doctor", "Doctor", options.doctors],
  ];
  const active = searchInput || Object.values(filters).some(Boolean);

  return (
    <section className="filters">
      <input
        type="search"
        className="search"
        placeholder="Search patient by name..."
        value={searchInput}
        onChange={(e) => onSearchChange(e.target.value)}
        aria-label="Search patients by name"
      />
      {selects.map(([key, label, list]) => (
        <select
          key={key}
          value={filters[key]}
          onChange={(e) => onFilterChange(key, e.target.value)}
          aria-label={`Filter by ${label}`}
        >
          <option value="">All {label}s</option>
          {list.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
      ))}
      {active && (
        <button className="btn btn-ghost" onClick={onClear}>
          Clear filters
        </button>
      )}
    </section>
  );
}