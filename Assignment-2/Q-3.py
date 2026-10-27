import mysql.connector
from mysql.connector import Error
import csv
import sys


def connect_database(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if conn.is_connected():
            print("Database connected successfully")
            return conn

    except Error as e:
        print("Database Error:", e)
        return None


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student (
            student_id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            spi DECIMAL(3,1) NOT NULL
        )
    """)
    

    conn.commit()
    cursor.close()


def insert_students(conn, filename):
    cursor = conn.cursor()

    query = """
        INSERT INTO Student (student_id, name, spi)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            spi = VALUES(spi)
    """

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        batch = []

        for row in reader:
            if not row:
                continue

            student_id, name, spi = row

            batch.append(
                (int(student_id), name, float(spi))
            )

            if len(batch) >= 1000:
                cursor.executemany(query, batch)
                conn.commit()
                batch.clear()

        if batch:
            cursor.executemany(query, batch)
            conn.commit()

    cursor.close()


def insert_registrations(conn, filename):
    cursor = conn.cursor()

    query = """
        INSERT IGNORE INTO CourseRegistration
        (student_id, course_id)
        VALUES (%s, %s)
    """

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        batch = []

        for row in reader:
            if not row:
                continue

            student_id, course_id = row

            batch.append(
                (int(student_id), course_id)
            )

            if len(batch) >= 1000:
                cursor.executemany(query, batch)
                conn.commit()
                batch.clear()

        if batch:
            cursor.executemany(query, batch)
            conn.commit()

    cursor.close()


def find_students(conn, course_id, spi_threshold):
    cursor = conn.cursor()

    query = """
        SELECT s.student_id,
               s.name,
               s.spi,
               r.course_id
        FROM Student s
        JOIN CourseRegistration r
            ON s.student_id = r.student_id
        WHERE r.course_id = %s
          AND s.spi > %s
        ORDER BY s.spi DESC,
                 s.student_id ASC
    """

    cursor.execute(
        query,
        (course_id, spi_threshold)
    )

    for student_id, name, spi, course in cursor:
        print(
            student_id,
            name,
            spi,
            course
        )

    cursor.close()


def main():
    try:
        host = input("Host: ").strip()
        user = input("Username: ").strip()
        password = input("Password: ")
        database = input("Database: ").strip()

        student_file = input("Student CSV: ").strip()
        registration_file = input(
            "Registration CSV: "
        ).strip()

        course_id = input("Course ID: ").strip()
        spi_threshold = float(
            input("SPI threshold: ")
        )

        conn = connect_database(
            host,
            user,
            password,
            database
        )

        if conn is None:
            return

        try:
            create_tables(conn)

            insert_students(
                conn,
                student_file
            )

            insert_registrations(
                conn,
                registration_file
            )

            find_students(
                conn,
                course_id,
                spi_threshold
            )

        finally:
            conn.close()

    except FileNotFoundError:
        print("CSV file not found")

    except ValueError:
        print("Invalid input")

    except Error as e:
        print("Database Error:", e)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()