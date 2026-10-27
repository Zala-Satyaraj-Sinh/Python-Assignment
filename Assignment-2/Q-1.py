import re
import sys


# Allowed username characters:
# letters, digits, +, ., _, -
EMAIL_PATTERN = re.compile(
    r'(?<![A-Za-z0-9+._-])'
    r'([A-Za-z0-9+._-]+)'
    r'@'
    r'([A-Za-z0-9-]+)'
    r'\.(com|edu|org)'
    r'(?![A-Za-z0-9-])',
    re.IGNORECASE
)


def process_file(filename):
    # domain -> set of complete email addresses
    emails = {
        "com": set(),
        "edu": set(),
        "org": set()
    }

    with open(filename, "r", encoding="utf-8", errors="ignore") as file:

        for line in file:
            for match in EMAIL_PATTERN.finditer(line):
                username = match.group(1)
                domain_name = match.group(2)
                tld = match.group(3).lower()

                email = (
                    username
                    + "@"
                    + domain_name
                    + "."
                    + tld
                ).lower()

                # Extra validation of username
                if not username:
                    continue

                emails[tld].add(email)

    for tld in sorted(emails):
        unique_emails = emails[tld]

        if unique_emails:
            smallest = min(unique_emails)

            print(
                f"{tld} "
                f"{len(unique_emails)} "
                f"{smallest}"
            )


def main():
    if len(sys.argv) != 2:
        print("Usage: python email_extractor.py <file>")
        return

    filename = sys.argv[1]
    process_file(filename)


if __name__ == "__main__":
    main()