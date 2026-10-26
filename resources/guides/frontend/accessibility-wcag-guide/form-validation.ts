// Accessible form validation
function validateField(field: HTMLInputElement): boolean {
  const errorEl = document.getElementById(`${field.id}-error`);
  const isValid = field.checkValidity();

  field.setAttribute("aria-invalid", String(!isValid));

  if (!isValid && errorEl) {
    errorEl.textContent = field.validationMessage;
    errorEl.style.display = "block";
  } else if (errorEl) {
    errorEl.textContent = "";
    errorEl.style.display = "none";
  }

  return isValid;
}
