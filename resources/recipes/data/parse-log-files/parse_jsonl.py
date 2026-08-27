import json
from datetime import datetime
from collections import Counter


def parse_jsonl(path):
    level_counts = Counter()
    errors = 0

    with open(path, 'r', encoding='utf-8') as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                record['ts'] = datetime.fromisoformat(record['ts'].replace('Z', '+00:00'))
                level_counts[record.get('level', 'UNKNOWN')] += 1
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                errors += 1
                print(f'malformed line {n}: {line!r} ({e})')

    print('Level counts:', dict(level_counts))
    print(f'Parse errors: {errors}')


if __name__ == '__main__':
    parse_jsonl('app.jsonl')
