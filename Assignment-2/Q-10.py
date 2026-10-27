import pandas as pd
import matplotlib.pyplot as plt
import os
import sys


def main():
    # Input paths
    input_file = input("Enter CSV file path: ").strip()
    output_folder = input("Enter output folder path: ").strip()

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # -----------------------------
    # 1. Read CSV
    # -----------------------------
    df = pd.read_csv(input_file)

    # Columns other than enrollment and name are subjects
    subject_columns = [
        col for col in df.columns
        if col not in ["enrollment", "name"]
    ]

    # -----------------------------
    # 2. Clean missing/invalid marks
    # -----------------------------
    for subject in subject_columns:
        df[subject] = pd.to_numeric(df[subject], errors="coerce")

        # Keep marks within 0-100
        df.loc[
            (df[subject] < 0) | (df[subject] > 100),
            subject
        ] = pd.NA

        # Replace missing marks with subject average
        df[subject] = df[subject].fillna(df[subject].mean())

    # -----------------------------
    # 3. Subject-wise statistics
    # -----------------------------
    summary = pd.DataFrame({
        "Subject": subject_columns,
        "Average": [df[s].mean() for s in subject_columns],
        "Minimum": [df[s].min() for s in subject_columns],
        "Maximum": [df[s].max() for s in subject_columns]
    })

    # -----------------------------
    # 4. Calculate total and average
    # -----------------------------
    df["Total"] = df[subject_columns].sum(axis=1)
    df["Average"] = df[subject_columns].mean(axis=1)

    # -----------------------------
    # 5. Assign grades
    # -----------------------------
    def get_grade(avg):
        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F"

    df["Grade"] = df["Average"].apply(get_grade)

    # -----------------------------
    # 6. Save cleaned CSV
    # -----------------------------
    cleaned_file = os.path.join(
        output_folder,
        "cleaned_marks.csv"
    )

    df.to_csv(cleaned_file, index=False)

    # Save summary CSV
    summary_file = os.path.join(
        output_folder,
        "summary.csv"
    )

    summary.to_csv(summary_file, index=False)

    # -----------------------------
    # 7. Grade distribution chart
    # -----------------------------
    grade_counts = df["Grade"].value_counts()

    plt.figure(figsize=(8, 5))
    grade_counts.plot(kind="bar")
    plt.title("Grade Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Number of Students")
    plt.tight_layout()

    plt.savefig(
        os.path.join(output_folder, "grade_distribution.png")
    )
    plt.close()

    # -----------------------------
    # 8. Subject average chart
    # -----------------------------
    plt.figure(figsize=(8, 5))
    plt.bar(summary["Subject"], summary["Average"])

    plt.title("Subject-wise Average")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        os.path.join(output_folder, "subject_average.png")
    )
    plt.close()

    # -----------------------------
    # 9. Top performers chart
    # -----------------------------
    top_students = df.nlargest(10, "Average")

    plt.figure(figsize=(10, 5))
    plt.bar(
        top_students["name"],
        top_students["Average"]
    )

    plt.title("Top 10 Performers")
    plt.xlabel("Student")
    plt.ylabel("Average Marks")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        os.path.join(output_folder, "top_performers.png")
    )
    plt.close()

    print("\nProcessing completed successfully!")
    print("Files created:")
    print("cleaned_marks.csv")
    print("summary.csv")
    print("grade_distribution.png")
    print("subject_average.png")
    print("top_performers.png")


if __name__ == "__main__":
    main()