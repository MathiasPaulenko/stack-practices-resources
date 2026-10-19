// Form-associated custom element via ElementInternals.
// Participates in <form> submission and native validation.
// Usage: <rating-input name="rating" required></rating-input>
class RatingInput extends HTMLElement {
  static formAssociated = true;

  constructor() {
    super();
    this._internals = this.attachInternals();
    this.attachShadow({ mode: 'open' }).innerHTML = `
      <style>
        button { font-size: 1.25rem; background: none; border: none; cursor: pointer; color: #d1d5db; padding: 0 0.1rem; }
        button.filled { color: #f59e0b; }
      </style>
      <div id="stars" role="radiogroup" aria-label="Rating"></div>
    `;
    this.value = 0;
  }

  connectedCallback() {
    const stars = this.shadowRoot.getElementById('stars');
    for (let i = 1; i <= 5; i++) {
      const star = document.createElement('button');
      star.type = 'button';
      star.textContent = '★';
      star.dataset.value = i;
      stars.appendChild(star);
    }
    stars.addEventListener('click', (e) => {
      if (e.target.dataset.value) this.setValue(Number(e.target.dataset.value));
    });
    this.paint();
  }

  setValue(v) {
    this.value = v;
    this._internals.setFormValue(String(v));
    this._internals.setValidity(
      v > 0 ? {} : { customError: true },
      'Choose a rating'
    );
    this.paint();
  }

  paint() {
    this.shadowRoot
      .querySelectorAll('#stars button')
      .forEach((s) =>
        s.classList.toggle('filled', Number(s.dataset.value) <= this.value)
      );
  }

  formResetCallback() {
    this.setValue(0);
  }
}

customElements.define('rating-input', RatingInput);
