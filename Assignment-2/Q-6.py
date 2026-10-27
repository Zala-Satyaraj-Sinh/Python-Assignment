import sys
import re
from collections import defaultdict, deque


# Log format:
# timestamp user ip status
LOG_PATTERN = re.compile(
    r'^(\d{2}:\d{2})\s+(\S+)\s+(\S+)\s+(FAIL|SUCCESS)$'
)


def to_minutes(timestamp):
    h, m = map(int, timestamp.split(":"))
    return h * 60 + m


def main():
    input = sys.stdin.buffer.readline

    # X and T
    X, T = map(int, input().split())

    # Number of logs
    n = int(input())

    # user -> deque of (time, ip) for recent failures
    failures = defaultdict(deque)

    # user -> first suspicious success timestamp
    suspicious = {}

    for _ in range(n):
        line = input().decode().strip()

        match = LOG_PATTERN.match(line)

        # Ignore malformed lines
        if not match:
            continue

        timestamp, user, ip, status = match.groups()
        current_time = to_minutes(timestamp)

        if status == "FAIL":
            q = failures[user]

            # Remove failures outside the T-minute window
            while q and current_time - q[0][0] > T:
                q.popleft()

            q.append((current_time, ip))

        else:  # SUCCESS
            q = failures[user]

            # Remove failures outside the T-minute window
            while q and current_time - q[0][0] > T:
                q.popleft()

            # Need at least X failures
            if len(q) >= X:

                # Success must come from a different IP
                different_ip = any(
                    fail_ip != ip
                    for _, fail_ip in q
                )

                if different_ip and user not in suspicious:
                    suspicious[user] = timestamp

    # Lexicographic order of user IDs
    for user in sorted(suspicious):
        print(user, suspicious[user])


if __name__ == "__main__":
    main()