MOD = 1000000007

n, m = map(int, input().split())

# DP arrays for maximum score and number of ways
max_score = [-10**18] * m
ways = [0] * m

for i in range(n):
    row = input().split()

    new_score = [-10**18] * m
    new_ways = [0] * m

    for j in range(m):

        # Blocked cell
        if row[j] == "X":
            continue

        value = int(row[j])

        # Starting cell
        if i == 0 and j == 0:
            new_score[j] = value
            new_ways[j] = 1
            continue

        best = -10**18
        count = 0

        # From above
        if i > 0 and max_score[j] != -10**18:
            best = max_score[j]
            count = ways[j]

        # From left
        if j > 0 and new_score[j - 1] != -10**18:
            if new_score[j - 1] > best:
                best = new_score[j - 1]
                count = new_ways[j - 1]
            elif new_score[j - 1] == best:
                count = (count + new_ways[j - 1]) % MOD

        # From diagonal
        if i > 0 and j > 0 and max_score[j - 1] != -10**18:
            if max_score[j - 1] > best:
                best = max_score[j - 1]
                count = ways[j - 1]
            elif max_score[j - 1] == best:
                count = (count + ways[j - 1]) % MOD

        if best != -10**18:
            new_score[j] = best + value
            new_ways[j] = count

    max_score = new_score
    ways = new_ways


# Destination unreachable
if max_score[m - 1] == -10**18:
    print("IMPOSSIBLE")
else:
    print(max_score[m - 1], ways[m - 1] % MOD)