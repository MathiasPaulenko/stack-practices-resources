// Tab interface: only one tab is in the tab order at a time
class TabList {
  private tabs: HTMLElement[] = [];
  private activeIndex = 0;

  constructor(container: HTMLElement) {
    this.tabs = Array.from(container.querySelectorAll('[role="tab"]'));
    this.tabs.forEach((tab, index) => {
      tab.addEventListener("keydown", this.handleKeyDown.bind(this));
      tab.addEventListener("click", () => this.activate(index));
    });
    this.updateTabindex();
  }

  private updateTabindex() {
    this.tabs.forEach((tab, index) => {
      tab.tabIndex = index === this.activeIndex ? 0 : -1;
      tab.setAttribute("aria-selected", String(index === this.activeIndex));
    });
  }

  private activate(index: number) {
    this.activeIndex = index;
    this.updateTabindex();
    this.tabs[index].focus();
  }

  private handleKeyDown(e: KeyboardEvent) {
    switch (e.key) {
      case "ArrowRight":
        e.preventDefault();
        this.activate((this.activeIndex + 1) % this.tabs.length);
        break;
      case "ArrowLeft":
        e.preventDefault();
        this.activate((this.activeIndex - 1 + this.tabs.length) % this.tabs.length);
        break;
      case "Home":
        e.preventDefault();
        this.activate(0);
        break;
      case "End":
        e.preventDefault();
        this.activate(this.tabs.length - 1);
        break;
    }
  }
}
