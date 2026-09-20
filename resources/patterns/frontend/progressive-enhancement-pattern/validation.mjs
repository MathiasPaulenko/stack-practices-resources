// validation.mjs — the same rules the enhancement layer applies in the
// browser, exported as a pure function so Node can test them without a DOM.

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/**
 * Validate one field's value.
 * @param {{value: string, required?: boolean, type?: string, maxLength?: number}} field
 * @returns {{isValid: boolean, message: string}}
 */
export function validateValue({ value, required = false, type = 'text', maxLength = -1 }) {
  if (required && !value.trim()) {
    return { isValid: false, message: 'This field is required.' };
  }
  if (type === 'email' && value) {
    if (!EMAIL_RE.test(value)) {
      return { isValid: false, message: 'Please enter a valid email address.' };
    }
  }
  if (maxLength > 0 && value.length > maxLength) {
    return { isValid: false, message: `Maximum ${maxLength} characters.` };
  }
  return { isValid: true, message: '' };
}
