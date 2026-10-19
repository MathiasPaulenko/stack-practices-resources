// Autonomous custom element: shadow DOM, observed attributes, slots.
// Usage:
//   <user-card name="Ada Lovelace" role="Engineer" user-id="u-1">
//     <span slot="bio">First programmer</span>
//   </user-card>
class UserCard extends HTMLElement {
  static get observedAttributes() {
    return ['name', 'role'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
    this.shadowRoot
      .querySelector('button')
      .addEventListener('click', () => this.select());
  }

  attributeChangedCallback() {
    // Guard: shadow DOM may not have children yet on first render
    if (this.shadowRoot.querySelector('.name')) this.render();
  }

  select() {
    this.dispatchEvent(
      new CustomEvent('user-selected', {
        detail: { userId: this.getAttribute('user-id') },
        bubbles: true,
        composed: true,
      })
    );
  }

  render() {
    const name = this.getAttribute('name') || 'Anonymous';
    const role = this.getAttribute('role') || 'Member';
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          padding: var(--card-padding, 1rem);
          border: 1px solid var(--card-border, #e5e7eb);
          border-radius: 0.5rem;
          font-family: system-ui, sans-serif;
        }
        .name { margin: 0; font-size: 1.125rem; }
        .role { color: var(--card-muted, #6b7280); font-size: 0.875rem; }
        ::slotted(span) { display: block; margin-top: 0.5rem; }
        button { margin-top: 0.75rem; cursor: pointer; }
      </style>
      <p class="name">${name}</p>
      <p class="role">${role}</p>
      <slot name="bio"></slot>
      <button type="button">Select</button>
    `;
  }
}

customElements.define('user-card', UserCard);
