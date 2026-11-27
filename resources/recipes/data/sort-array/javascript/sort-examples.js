// Multi-key sort: age first, ties broken alphabetically.
export const byAgeThenName = (users) =>
  users.toSorted((a, b) => a.age - b.age || a.name.localeCompare(b.name));

// Numeric sort done right — never rely on the default comparator.
export const numericAsc = (nums) => nums.toSorted((a, b) => a - b);

// Push nulls to the end via a boolean sort key trick.
export const nullsLast = (values) =>
  values.toSorted((a, b) => (a === null) - (b === null) || a - b);
