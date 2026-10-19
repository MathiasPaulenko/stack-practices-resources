// Slots + CSS custom properties theming.
// Usage:
//   <alert-box type="error">
//     <h3 slot="title">Connection Failed</h3>
//     <p>Check your network and retry.</p>
//   </alert-box>
class AlertBox extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' });
    const type = this.getAttribute('type') || 'info';
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          padding: 1rem;
          border-radius: 0.5rem;
          border-left: 4px solid var(--alert-accent, #3b82f6);
          background: var(--alert-bg, #eff6ff);
          font-family: system-ui, sans-serif;
        }
        :host([type="error"]) {
          --alert-accent: #ef4444;
          --alert-bg: #fef2f2;
        }
        :host([type="success"]) {
          --alert-accent: #22c55e;
          --alert-bg: #f0fdf4;
        }
        ::slotted(h3) { margin: 0 0 0.25rem; }
        ::slotted(p) { margin: 0; }
      </style>
      <slot name="title"></slot>
      <slot></slot>
    `;
  }
}

customElements.define('alert-box', AlertBox);
