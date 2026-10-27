import os
import re
import pickle
import zipfile


def tokenize(line):
    return re.findall(r"[A-Za-z0-9_]+", line.lower())


def build(folder, zip_name):
    index = {}
    total_files = 0
    total_lines = 0

    for filename in sorted(os.listdir(folder)):
        path = os.path.join(folder, filename)

        if not os.path.isfile(path):
            continue

        total_files += 1

        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            for line_no, line in enumerate(file, 1):
                total_lines += 1

                # Avoid adding the same token twice for one line
                tokens = set(tokenize(line))

                for token in tokens:
                    if token not in index:
                        index[token] = []

                    index[token].append((filename, line_no))

    # Create pickle file
    pickle_path = os.path.splitext(zip_name)[0] + ".pkl"

    with open(pickle_path, "wb") as file:
        pickle.dump(index, file)

    # Create ZIP containing logs and pickle
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as archive:

        for filename in sorted(os.listdir(folder)):
            path = os.path.join(folder, filename)

            if os.path.isfile(path):
                archive.write(path, filename)

        archive.write(pickle_path, os.path.basename(pickle_path))

    print("FILES", total_files)
    print("LINES", total_lines)
    print("TOKENS", len(index))


def search(pickle_path, queries):
    with open(pickle_path, "rb") as file:
        index = pickle.load(file)

    for query in queries:
        token = query.lower()

        if token in index:
            for filename, line_no in index[token]:
                print(f"{filename}:{line_no}")
        else:
            print("NOT FOUND")


def main():
    parts = input().split()

    if not parts:
        print("Invalid input")
        return

    mode = parts[0].upper()

    if mode == "BUILD":

        if len(parts) != 3:
            print("Invalid input")
            return

        folder = parts[1]
        zip_name = parts[2]

        build(folder, zip_name)

    elif mode == "SEARCH":

        if len(parts) < 3:
            print("Invalid input")
            return

        pickle_path = parts[1]
        q = int(parts[2])

        if len(parts) != 3 + q:
            print("Invalid input")
            return

        queries = parts[3:]

        search(pickle_path, queries)

    else:
        print("Invalid input")


if __name__ == "__main__":
    main()