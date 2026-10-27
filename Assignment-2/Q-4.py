import mysql.connector


# Whitelisted columns
ALLOWED_COLUMNS = {
    "student.id": "s.student_id",
    "student.name": "s.name",
    "student.spi": "s.spi",
    "course.id": "c.course_id",
    "course.name": "c.course_name",
    "course.credits": "c.credits",
    "registration.student_id": "cr.student_id",
    "registration.course_id": "cr.course_id"
}

ALLOWED_ORDER_COLUMNS = {
    "student.id": "s.student_id",
    "student.name": "s.name",
    "student.spi": "s.spi",
    "course.id": "c.course_id",
    "course.name": "c.course_name"
}


def build_query(columns, filters, order_column, direction, limit):
    # Validate selected columns
    if not columns:
        raise ValueError("No columns selected")

    selected = []

    for col in columns:
        col = col.strip()

        if col not in ALLOWED_COLUMNS:
            raise ValueError(f"Invalid column: {col}")

        selected.append(ALLOWED_COLUMNS[col])

    # Validate limit
    try:
        limit = int(limit)
    except ValueError:
        raise ValueError("Limit must be an integer")

    if not 1 <= limit <= 1000:
        raise ValueError("Limit must be between 1 and 1000")

    # Validate order column
    if order_column not in ALLOWED_ORDER_COLUMNS:
        raise ValueError("Invalid order column")

    direction = direction.upper()

    if direction not in ("ASC", "DESC"):
        raise ValueError("Invalid sort direction")

    sql = f"""
SELECT {', '.join(selected)}
FROM Student s
JOIN CourseRegistration cr
    ON s.student_id = cr.student_id
JOIN Course c
    ON cr.course_id = c.course_id
"""

    parameters = []
    conditions = []

    # Process filters
    for column, operator, value in filters:
        column = column.strip().lower()
        operator = operator.upper()

        if column not in ALLOWED_COLUMNS:
            raise ValueError(f"Invalid filter column: {column}")

        if operator not in ("=", "<", ">", "<=", ">=", "<>", "LIKE"):
            raise ValueError(f"Invalid operator: {operator}")

        conditions.append(f"{ALLOWED_COLUMNS[column]} {operator} %s")
        parameters.append(value)

    if conditions:
        sql += "WHERE " + " AND ".join(conditions) + "\n"

    sql += f"ORDER BY {ALLOWED_ORDER_COLUMNS[order_column]} {direction}\n"
    sql += "LIMIT %s"

    parameters.append(limit)

    return sql, parameters


def main():
    try:
        # Example input
        columns = ["student.name", "course.name"]

        filters = [
            ("course.id", "=", "PY101")
        ]

        order_column = "student.spi"
        direction = "DESC"
        limit = 2

        sql, parameters = build_query(
            columns,
            filters,
            order_column,
            direction,
            limit
        )

        print("SQL_OK")
        print("\nGenerated SQL:")
        print(sql)

        print("Parameters:", parameters)

        # Connect to MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sm@2/11/2006",
            database="College"
        )

        cursor = conn.cursor()

        cursor.execute(sql, parameters)

        print("\nResults:")

        for row in cursor.fetchall():
            print(*row)

        cursor.close()
        conn.close()

    except (ValueError, mysql.connector.Error) as e:
        print("ERROR:", e)


if __name__ == "__main__":
    main()