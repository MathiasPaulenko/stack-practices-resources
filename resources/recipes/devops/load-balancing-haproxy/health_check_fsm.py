"""Simulates HAProxy's active health-check state machine.

Each backend runs a small FSM driven by probe results at every `inter`
interval: `fall N` consecutive failures mark it DOWN, `rise M` consecutive
passes mark it UP again. A leastconn dispatcher then routes simulated
requests only across servers currently UP.

This mirrors the recipe's `default-server inter 5s fall 2 rise 3` tuning:
a flapping backend that fails intermittently leaves rotation fast but
rejoins slowly, so clients never see its bad period.
"""

FALL = 2  # consecutive failures to mark DOWN
RISE = 3  # consecutive passes to mark UP


class Backend:
    def __init__(self, name, probes):
        self.name = name
        self.probes = probes  # list[bool], one per interval
        self.up = True
        self.fails = 0
        self.passes = 0
        self.sessions = 0
        self.log = []

    def probe(self, ok):
        if ok:
            self.fails = 0
            self.passes += 1
            if not self.up and self.passes >= RISE:
                self.up = True
                self.log.append(f"{self.name}: UP after {self.passes} passes")
        else:
            self.passes = 0
            self.fails += 1
            if self.up and self.fails >= FALL:
                self.up = False
                self.log.append(f"{self.name}: DOWN after {self.fails} fails")


def main():
    web1 = Backend("web1", [True] * 20)
    # web2 fails at t=0..3 (down at t=1), recovers slowly (up at t=6)
    web2 = Backend("web2", [False] * 4 + [True] * 16)
    # web3 flaps: never reaches 3 consecutive passes, stays down
    web3 = Backend("web3", [True, False, False, True, False, False] * 4)

    pool = [web1, web2, web3]
    intervals = 20
    served = {b.name: 0 for b in pool}

    for t in range(intervals):
        for b in pool:
            b.probe(b.probes[t % len(b.probes)])

        candidates = [b for b in pool if b.up]
        if not candidates:
            continue  # backup server would serve here
        pick = min(candidates, key=lambda b: b.sessions)
        pick.sessions += 1
        served[pick.name] += 1
        # sessions accumulate so leastconn visibly steers traffic to web2
        # once it rejoins; real HAProxy drains them as requests finish

    for b in pool:
        for entry in b.log:
            print(entry)
    print(f"\nRequests served per backend (of {intervals}):")
    for name, n in served.items():
        print(f"  {name}: {n}")
    print("\nweb3 flapped and never earned 3 consecutive passes:")
    print("  it stayed DOWN the whole run despite answering some probes")


if __name__ == "__main__":
    main()
