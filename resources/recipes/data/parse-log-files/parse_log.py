import re
from collections import Counter

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) (?P<proto>[^"]+)" '
    r'(?P<status>\d{3}) (?P<bytes>\S+)'
)


def parse_apache_log(path):
    status_counts = Counter()
    parse_errors = 0
    total = 0

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            total += 1
            match = LOG_PATTERN.match(line)
            if match:
                status_counts[match.group('status')] += 1
            else:
                parse_errors += 1
                print(f'malformed line {total}: {line.rstrip()[:120]}')

    print('\nStatus counts:', dict(status_counts))
    print(f'Parse errors: {parse_errors}/{total} ({100 * parse_errors / total:.2f}%)')


if __name__ == '__main__':
    parse_apache_log('access.log')
