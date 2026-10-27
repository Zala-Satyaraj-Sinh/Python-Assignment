class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False


def insert(root, word):
    node = root

    for ch in word.lower():
        if ch not in node.children:
            node.children[ch] = TrieNode()
        node = node.children[ch]

    node.end = True


def contains_banned(password, root):
    password = password.lower()

    # Try every position as the starting point
    for i in range(len(password)):
        node = root

        for j in range(i, len(password)):
            ch = password[j]

            if ch not in node.children:
                break

            node = node.children[ch]

            if node.end:
                return True

    return False


# Number of banned words
b = int(input())

root = TrieNode()

# Store banned words
for _ in range(b):
    word = input().strip()
    insert(root, word)

# Number of passwords
n = int(input())

for index in range(1, n + 1):
    password = input().strip()

    # Check length
    if len(password) < 6 or len(password) > 12:
        print(f"{index}: WEAK_LENGTH")
        continue

    # Check character requirements
    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False

    for ch in password:
        if ch.islower():
            has_lower = True
        elif ch.isupper():
            has_upper = True
        elif ch.isdigit():
            has_digit = True
        elif ch in "$#@":
            has_special = True

    # Check repeated character more than 3 times
    repeated = False
    count = 1

    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            count += 1

            if count > 3:
                repeated = True
                break
        else:
            count = 1

    if repeated:
        print(f"{index}: WEAK_PATTERN")
        continue

    # Check banned words
    if contains_banned(password, root):
        print(f"{index}: COMPROMISED")
        continue

    # Check all strong-password requirements
    if has_lower and has_upper and has_digit and has_special:
        print(f"{index}: STRONG")
    else:
        print(f"{index}: WEAK_PATTERN")