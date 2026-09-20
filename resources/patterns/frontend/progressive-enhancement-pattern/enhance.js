// enhance.js — enhancement layer. The page works if this file never runs.
document.documentElement.classList.add('js');

// --- Inline validation + async submit ---
const form = document.querySelector('.contact-form');

if (form && window.peFeatures && window.peFeatures.fetch) {
  const inputs = form.querySelectorAll('input, textarea');

  inputs.forEach((input) => {
    input.addEventListener('blur', () => validateField(input));
    input.addEventListener('input', () => {
      if (input.classList.contains('invalid')) validateField(input);
    });
  });

  function validateField(input) {
    const field = input.closest('.field');
    let isValid = true;
    let message = '';

    if (input.required && !input.value.trim()) {
      isValid = false;
      message = 'This field is required.';
    } else if (input.type === 'email' && input.value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(input.value)) {
        isValid = false;
        message = 'Please enter a valid email address.';
      }
    } else if (input.maxLength > 0 && input.value.length > input.maxLength) {
      isValid = false;
      message = `Maximum ${input.maxLength} characters.`;
    }

    field.classList.toggle('invalid', !isValid);

    let errorEl = field.querySelector('.error-message');
    if (!errorEl) {
      errorEl = document.createElement('span');
      errorEl.className = 'error-message';
      field.appendChild(errorEl);
    }
    errorEl.textContent = message;

    return isValid;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    let allValid = true;
    inputs.forEach((input) => {
      if (!validateField(input)) allValid = false;
    });
    if (!allValid) return;

    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.textContent = 'Sending...';

    try {
      const response = await fetch(form.action, {
        method: form.method,
        body: new FormData(form),
      });

      if (response.ok) {
        form.innerHTML = `
          <div class="success-message">
            <h2>Thank you!</h2>
            <p>Your message has been sent.</p>
          </div>
        `;
      } else {
        throw new Error('Server error');
      }
    } catch {
      // The demo endpoint does not exist; restore the button and let the
      // user retry. A real app could fall back to a normal form post here.
      submitButton.disabled = false;
      submitButton.textContent = 'Send Message';
      const errorDiv = document.createElement('div');
      errorDiv.className = 'form-error';
      errorDiv.textContent = 'Failed to send. Please try again.';
      form.insertBefore(errorDiv, form.firstChild);
    }
  });
}

// --- Click-to-sort table ---
document.querySelectorAll('table[data-enhance="sort"]').forEach((table) => {
  const headers = table.querySelectorAll('th[data-sort]');

  headers.forEach((header) => {
    header.setAttribute('role', 'button');
    header.setAttribute('tabindex', '0');

    header.addEventListener('click', () => sortTable(table, header));
    header.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        sortTable(table, header);
      }
    });
  });

  function sortTable(table, header) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const currentDir = header.dataset.dir || 'asc';
    const newDir = currentDir === 'asc' ? 'desc' : 'asc';

    rows.sort((a, b) => {
      const aVal = a
        .querySelector(`td:nth-child(${header.cellIndex + 1})`)
        .textContent;
      const bVal = b
        .querySelector(`td:nth-child(${header.cellIndex + 1})`)
        .textContent;
      return newDir === 'asc'
        ? aVal.localeCompare(bVal)
        : bVal.localeCompare(aVal);
    });

    header.dataset.dir = newDir;
    rows.forEach((row) => tbody.appendChild(row));
  }
});
