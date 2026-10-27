n, k, m = map(int, input().split())

students = []
semesters = {}

for _ in range(n):
    data = input().split()

    enrollment = data[0]
    name = data[1]
    semester = int(data[2])
    cpi = float(data[3])
    marks = list(map(int, data[4:]))

    student = {
        "enrollment": enrollment,
        "name": name,   
        "semester": semester,
        "cpi": cpi,
        "marks": marks
    }

    students.append(student)
    semesters.setdefault(semester, []).append(student)


# Semester-wise top K students
for sem in sorted(semesters):
    group = semesters[sem]

    # CPI descending, average marks descending,
    # enrollment ascending
    group.sort(
        key=lambda s: (
            -s["cpi"],
            -sum(s["marks"]) / m,
            s["enrollment"]
        )
    )

    top_k = group[:k]

    print(f"Semester {sem}:", *[s["enrollment"] for s in top_k])


# Subject-wise toppers
for j in range(m):
    max_mark = max(s["marks"][j] for s in students)

    toppers = [
        s["enrollment"]
        for s in students
        if s["marks"][j] == max_mark
    ]

    print(f"S{j + 1}:", *toppers)