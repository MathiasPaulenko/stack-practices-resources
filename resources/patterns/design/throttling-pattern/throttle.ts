class Throttle {
  private requests: number[] = [];

  constructor(private maxRequests: number, private windowMs: number) {}

  canProceed(): boolean {
    const now = Date.now();
    this.requests = this.requests.filter(t => now - t < this.windowMs);
    if (this.requests.length < this.maxRequests) {
      this.requests.push(now);
      return true;
    }
    return false;
  }

  timeUntilNextSlot(): number {
    if (this.requests.length < this.maxRequests) return 0;
    return this.windowMs - (Date.now() - this.requests[0]);
  }
}

const throttle = new Throttle(10, 1000);

async function geocode(address: string): Promise<LatLng> {
  if (!throttle.canProceed()) {
    await new Promise(r => setTimeout(r, throttle.timeUntilNextSlot()));
  }
  const res = await fetch(
    `https://maps.googleapis.com/maps/api/geocode/json?address=${address}`
  );
  return res.json();
}
