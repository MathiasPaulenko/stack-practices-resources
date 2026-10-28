"""Cache strategy decision record generator (stdlib only).

Companion to https://stackpractices.com/docs/cache-strategy-decision-template/

Interactive CLI that asks the same questions as the decision tree, then emits
a filled CACHE STRATEGY DECISION RECORD you can paste into a service doc or ADR.

Run: python src/decision_generator.py
"""

STRATEGIES = ("no-cache", "cache-aside", "read-through",
              "write-through", "write-back", "refresh-ahead")


def ask(prompt: str, default: str = "") -> str:
    answer = input(f"{prompt} [{default}]: ").strip()
    return answer or default


def ask_yn(prompt: str) -> bool:
    return ask(prompt + " (y/n)", "n").lower().startswith("y")


def decide(changes_fast: bool, write_heavy: bool, loss_ok: bool,
           predictable: bool, strong_writes: bool) -> str:
    """Same order as the decision tree in the template."""
    if changes_fast:
        return "no-cache"
    if write_heavy:
        return "write-back" if loss_ok else "write-through"
    if predictable:
        return "refresh-ahead"
    if strong_writes:
        return "write-through"
    return "cache-aside"


def render_record(facts: dict[str, str], strategy: str, rationale: str) -> str:
    return f"""CACHE STRATEGY DECISION RECORD
{'─' * 54}
Service / endpoint : {facts['service']} — {facts['resource']}
Data owner         : {facts['owner']}
Date / author      : {facts['date']} / {facts['author']}

WORKLOAD FACTS (measured, not guessed)
  Read:write ratio       : {facts['ratio']}
  Peak QPS on resource   : {facts['qps']}
  p95 latency budget     : {facts['p95']}
  Data change frequency  : {facts['freq']}
  Staleness tolerance    : {facts['stale']}
  Loss tolerance         : {facts['loss']}

DECISION
  Strategy               : {strategy}
  TTL                    : {facts['ttl']} + jitter ±10%
  Invalidation           : {facts['invalidation']}
  Stampede protection    : {facts['stampede']}
  Fallback on cache down : {facts['fallback']}

RATIONALE
  Why this strategy      : {rationale}
  Rejected alternatives  : {facts['rejected']}
  Review trigger         : {facts['review']}
"""


def main() -> None:
    print("Cache strategy decision record generator\n")
    facts = {
        "service": ask("Service / endpoint"),
        "resource": ask("Cacheable resource", "entity:<id>"),
        "owner": ask("Data owner (team)"),
        "date": ask("Date (YYYY-MM-DD)"),
        "author": ask("Author"),
        "ratio": ask("Read:write ratio", "95:5"),
        "qps": ask("Peak QPS on resource", "500"),
        "p95": ask("p95 latency budget added by miss (ms)", "50"),
        "freq": ask("Data change frequency", "every ~10 min"),
        "stale": ask("Staleness tolerance", "60 s"),
        "loss": ask("Loss tolerance", "writes are reconstructible"),
        "ttl": ask("TTL (seconds)", "600"),
        "invalidation": ask("Invalidation", "explicit delete on update"),
        "stampede": ask("Stampede protection", "lock"),
        "fallback": ask("Fallback on cache down", "serve stale"),
        "rejected": ask("Rejected alternatives", "write-back — loss window not acceptable"),
        "review": ask("Review trigger", "hit ratio < 90% for 7 days"),
    }

    strategy = decide(
        changes_fast=ask_yn("Does data change faster than the cache fills?"),
        write_heavy=ask_yn("Is the workload write-heavy (>70% writes)?"),
        loss_ok=ask_yn("Tolerate lost writes on a cache crash?"),
        predictable=ask_yn("Predictable hot keys?"),
        strong_writes=ask_yn("Need strong consistency on writes?"),
    )
    rationale = ask("Why this strategy", "fits the workload facts above")

    print("\n" + render_record(facts, strategy, rationale))


if __name__ == "__main__":
    main()
