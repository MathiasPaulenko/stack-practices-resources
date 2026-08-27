import re

SYSLOG_PATTERN = re.compile(
    r'<(?P<priority>\d+)>'
    r'(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+'
    r'(?P<host>\S+)\s+'
    r'(?P<message>.+)'
)


def parse_syslog(path):
    errors = 0
    with open(path, 'r', encoding='utf-8') as f:
        for n, line in enumerate(f, 1):
            match = SYSLOG_PATTERN.match(line)
            if match:
                record = match.groupdict()
                print(f'{n}: priority={record["priority"]} host={record["host"]} msg={record["message"][:80]}')
            else:
                errors += 1
                print(f'malformed line {n}: {line.rstrip()[:120]}')
    print(f'Parse errors: {errors}')


if __name__ == '__main__':
    parse_syslog('syslog.log')
