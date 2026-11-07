// Type-safe state machine.
// Event names are collected via a mapped type indexed by its own keys:
// { [K in keyof T]: keyof T[K]["transitions"] }[keyof T]
// The naive version — T[keyof T]["transitions"] & string — collapses to never.

export type StateMachine<T extends Record<string, { transitions: Record<string, string> }>> = {
  [K in keyof T]: { state: K; transitions: keyof T[K]["transitions"] };
};

export type TrafficLight = {
  red: { transitions: { go: "green" } };
  green: { transitions: { warn: "yellow" } };
  yellow: { transitions: { stop: "red" } };
};

export type TrafficState = StateMachine<TrafficLight>[keyof StateMachine<TrafficLight>];

export type EventsOf<T extends Record<string, { transitions: Record<string, string> }>> =
  { [K in keyof T]: keyof T[K]["transitions"] }[keyof T];

export class Machine<T extends Record<string, { transitions: Record<string, string> }>> {
  constructor(private current: keyof T, private config: T) {}

  transition(event: EventsOf<T>): void {
    const stateConfig = this.config[this.current];
    const next = stateConfig.transitions[event as string];
    if (!next) {
      throw new Error(`Invalid transition: ${String(event)} from ${String(this.current)}`);
    }
    this.current = next as keyof T;
  }

  get state(): keyof T {
    return this.current;
  }
}
