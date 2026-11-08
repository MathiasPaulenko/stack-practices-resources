"""Event burst simulation: debounce vs throttle over a synthetic event stream.

Run: python src/debounce_throttle_simulation.py
"""

DEBOUNCE_WAIT = 250  # ms
THROTTLE_LIMIT = 300  # ms


def simulate(events: list[int]) -> None:
    throttle_last = float("-inf")
    throttle_fires = 0
    quiet_start = None
    debounce_fires = 0

    for t in events:
        if t - throttle_last >= THROTTLE_LIMIT:
            throttle_last = t
            throttle_fires += 1
        # Debounce: a quiet gap >= wait since the last event closes a burst.
        if quiet_start is not None and t - quiet_start >= DEBOUNCE_WAIT:
            debounce_fires += 1
        quiet_start = t
    debounce_fires += 1

    print(
        f"events={len(events)}  raw={len(events)}  "
        f"debounce={debounce_fires}  throttle={throttle_fires}"
    )


def main() -> None:
    # Burst of 12 events in ~300ms, a pause, then 3 more.
    events = [i * 25 for i in range(12)] + [1000, 1050, 1100]
    simulate(events)


if __name__ == "__main__":
    main()
