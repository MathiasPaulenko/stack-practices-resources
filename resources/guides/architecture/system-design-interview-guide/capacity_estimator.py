"""Back-of-the-envelope capacity estimator for system design interviews.

Feed it daily volumes and a record size; it prints the numbers you would
say out loud on the whiteboard: writes/s, reads/s, daily and yearly storage.
"""

from dataclasses import dataclass

SECONDS_PER_DAY = 86_400
DAYS_PER_YEAR = 365
PEAK_FACTOR = 3  # assume peak traffic is ~3x the daily average


@dataclass
class Estimate:
    writes_per_day: int
    reads_per_day: int
    record_bytes: int

    @property
    def writes_per_second(self) -> float:
        return self.writes_per_day / SECONDS_PER_DAY

    @property
    def reads_per_second(self) -> float:
        return self.reads_per_day / SECONDS_PER_DAY

    @property
    def daily_storage_gb(self) -> float:
        return self.writes_per_day * self.record_bytes / 1e9

    @property
    def yearly_storage_tb(self) -> float:
        return self.daily_storage_gb * DAYS_PER_YEAR / 1000


def report(e: Estimate) -> None:
    rw_ratio = e.reads_per_day / e.writes_per_day
    print(f"Writes : {e.writes_per_day:,}/day  ~ {e.writes_per_second:,.0f}/s"
          f" (peak ~{e.writes_per_second * PEAK_FACTOR:,.0f}/s)")
    print(f"Reads  : {e.reads_per_day:,}/day  ~ {e.reads_per_second:,.0f}/s"
          f" (peak ~{e.reads_per_second * PEAK_FACTOR:,.0f}/s)")
    print(f"R/W ratio: {rw_ratio:.0f}:1")
    print(f"Storage: {e.daily_storage_gb:,.0f} GB/day "
          f"~ {e.yearly_storage_tb:,.0f} TB/year "
          f"(~{e.yearly_storage_tb * 5:,.0f} TB over 5 years)")


if __name__ == "__main__":
    # URL shortener numbers from the guide: 100M writes/day, 10B reads/day,
    # ~600 B per record (short_code 6 B + long_url 500 B + metadata ~100 B).
    report(Estimate(writes_per_day=100_000_000,
                    reads_per_day=10_000_000_000,
                    record_bytes=600))
