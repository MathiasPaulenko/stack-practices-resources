// Mediator pattern: multi-step checkout wizard. Run: npx tsx checkout-wizard.ts
interface WizardMediator {
  notify(sender: string, event: string, data?: unknown): void;
}

abstract class WizardStep {
  constructor(protected mediator: WizardMediator, public name: string) {}
  abstract render(): string;
  abstract validate(): boolean;
}

class PersonalInfoStep extends WizardStep {
  private data = { name: "", email: "" };
  render() { return `<input name="name" /><input name="email" />`; }
  validate() {
    if (!this.data.name || !this.data.email) return false;
    this.mediator.notify(this.name, "valid", this.data);
    return true;
  }
}

class AddressStep extends WizardStep {
  private data = { street: "", city: "" };
  render() { return `<input name="street" /><input name="city" />`; }
  validate() {
    if (!this.data.street || !this.data.city) return false;
    this.mediator.notify(this.name, "valid", this.data);
    return true;
  }
}

class PaymentStep extends WizardStep {
  private data = { card: "", cvv: "" };
  render() { return `<input name="card" /><input name="cvv" />`; }
  validate() {
    if (this.data.card.length < 16) return false;
    this.mediator.notify(this.name, "valid", this.data);
    return true;
  }
}

class CheckoutWizard implements WizardMediator {
  private steps: WizardStep[] = [];
  private currentStep = 0;
  private collectedData: Record<string, unknown> = {};

  constructor() {
    this.steps = [
      new PersonalInfoStep(this, "personal"),
      new AddressStep(this, "address"),
      new PaymentStep(this, "payment"),
    ];
  }

  notify(sender: string, event: string, data?: unknown) {
    if (event === "valid") {
      this.collectedData[sender] = data;
      this.next();
    }
  }

  next() {
    if (this.currentStep < this.steps.length - 1) {
      this.currentStep++;
      this.renderCurrent();
    } else {
      this.complete();
    }
  }

  back() {
    if (this.currentStep > 0) { this.currentStep--; this.renderCurrent(); }
  }

  renderCurrent(): string { return this.steps[this.currentStep].render(); }
  validateCurrent(): boolean { return this.steps[this.currentStep].validate(); }
  complete() { console.log("Wizard complete:", this.collectedData); }
}

const wizard = new CheckoutWizard();
console.log(wizard.renderCurrent());
