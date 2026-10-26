class AccessibleModal {
  private dialog: HTMLDialogElement;
  private previouslyFocused: HTMLElement | null = null;

  constructor(dialog: HTMLDialogElement) {
    this.dialog = dialog;
    dialog.addEventListener("close", this.onClose.bind(this));
    dialog.addEventListener("keydown", this.onKeyDown.bind(this));
  }

  open() {
    this.previouslyFocused = document.activeElement as HTMLElement;
    this.dialog.showModal();
    const firstFocusable = this.dialog.querySelector(
      "button, [href], input, select, textarea, [tabindex]:not([tabindex='-1'])"
    ) as HTMLElement;
    firstFocusable?.focus();
  }

  close() {
    this.dialog.close();
  }

  private onClose() {
    // Return focus to the element that opened the modal
    this.previouslyFocused?.focus();
  }

  private onKeyDown(e: KeyboardEvent) {
    if (e.key === "Escape") {
      this.close();
      return;
    }

    // Focus trap: keep focus within the dialog
    if (e.key !== "Tab") return;

    const focusables = Array.from(
      this.dialog.querySelectorAll<HTMLElement>(
        "button, [href], input, select, textarea, [tabindex]:not([tabindex='-1'])"
      )
    ).filter((el) => !el.hasAttribute("disabled"));

    if (focusables.length === 0) return;

    const first = focusables[0];
    const last = focusables[focusables.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }
}
