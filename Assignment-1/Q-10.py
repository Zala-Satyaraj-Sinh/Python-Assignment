import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os


DATA_FILE = "submissions.json"


class AssignmentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Assignment Manager")
        self.root.geometry("1000x650")

        self.records = []
        self.load_data()

        # -------------------------
        # Student Details
        # -------------------------
        student_frame = ttk.LabelFrame(root, text="Student Details")
        student_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(student_frame, text="Enrollment:").grid(
            row=0, column=0, padx=5, pady=5
        )

        self.enrollment_entry = ttk.Entry(student_frame, width=20)
        self.enrollment_entry.grid(row=0, column=1, padx=5)

        ttk.Label(student_frame, text="Name:").grid(
            row=0, column=2, padx=5
        )

        self.name_entry = ttk.Entry(student_frame, width=25)
        self.name_entry.grid(row=0, column=3, padx=5)

        # -------------------------
        # Assignment Details
        # -------------------------
        assignment_frame = ttk.LabelFrame(root, text="Assignment Details")
        assignment_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(assignment_frame, text="Assignment:").grid(
            row=0, column=0, padx=5, pady=5
        )

        self.assignment_entry = ttk.Entry(assignment_frame, width=25)
        self.assignment_entry.grid(row=0, column=1, padx=5)

        ttk.Label(assignment_frame, text="Marks:").grid(
            row=0, column=2, padx=5
        )

        self.marks_entry = ttk.Entry(assignment_frame, width=10)
        self.marks_entry.grid(row=0, column=3, padx=5)

        ttk.Label(assignment_frame, text="Remarks:").grid(
            row=0, column=4, padx=5
        )

        self.remarks_entry = ttk.Entry(assignment_frame, width=25)
        self.remarks_entry.grid(row=0, column=5, padx=5)

        # -------------------------
        # Buttons
        # -------------------------
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Add Submission",
            command=self.add_submission
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame,
            text="Update Marks",
            command=self.update_marks
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            button_frame,
            text="Export CSV",
            command=self.export_csv
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields
        ).grid(row=0, column=3, padx=5)

        # -------------------------
        # Filter
        # -------------------------
        filter_frame = ttk.Frame(root)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Filter Status:").pack(side="left")

        self.filter_combo = ttk.Combobox(
            filter_frame,
            values=["All", "Pending", "Completed"],
            state="readonly",
            width=15
        )
        self.filter_combo.set("All")
        self.filter_combo.pack(side="left", padx=10)
        self.filter_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_table()
        )

        # -------------------------
        # Table
        # -------------------------
        table_frame = ttk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = (
            "Enrollment",
            "Name",
            "Assignment",
            "Status",
            "Marks",
            "Remarks"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=140)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.load_selected_record
        )

        self.refresh_table()

    # -------------------------
    # Load JSON
    # -------------------------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    self.records = json.load(file)
            except (json.JSONDecodeError, OSError):
                self.records = []
        else:
            self.records = []

    # -------------------------
    # Save JSON
    # -------------------------
    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.records, file, indent=4)

    # -------------------------
    # Validation
    # -------------------------
    def validate_fields(self):
        enrollment = self.enrollment_entry.get().strip()
        name = self.name_entry.get().strip()
        assignment = self.assignment_entry.get().strip()
        marks = self.marks_entry.get().strip()

        if not enrollment:
            messagebox.showerror("Error", "Enrollment is required")
            return False

        if not name:
            messagebox.showerror("Error", "Name is required")
            return False

        if not assignment:
            messagebox.showerror("Error", "Assignment is required")
            return False

        if marks:
            try:
                marks_value = float(marks)

                if marks_value < 0 or marks_value > 100:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Marks must be a number between 0 and 100"
                )
                return False

        return True

    # -------------------------
    # Add Submission
    # -------------------------
    def add_submission(self):
        if not self.validate_fields():
            return

        enrollment = self.enrollment_entry.get().strip()
        name = self.name_entry.get().strip()
        assignment = self.assignment_entry.get().strip()
        marks = self.marks_entry.get().strip()
        remarks = self.remarks_entry.get().strip()

        if marks:
            marks = float(marks)
            status = "Completed"
        else:
            marks = ""
            status = "Pending"

        record = {
            "enrollment": enrollment,
            "name": name,
            "assignment": assignment,
            "status": status,
            "marks": marks,
            "remarks": remarks
        }

        self.records.append(record)
        self.save_data()
        self.refresh_table()
        self.clear_fields()

        messagebox.showinfo("Success", "Submission added successfully")

    # -------------------------
    # Update Marks
    # -------------------------
    def update_marks(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showerror(
                "Error",
                "Select a submission first"
            )
            return

        marks = self.marks_entry.get().strip()

        if not marks:
            messagebox.showerror(
                "Error",
                "Enter marks"
            )
            return

        try:
            marks = float(marks)

            if marks < 0 or marks > 100:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Marks must be between 0 and 100"
            )
            return

        item = self.tree.item(selected[0])
        values = item["values"]

        enrollment = str(values[0])
        assignment = str(values[2])

        for record in self.records:
            if (
                record["enrollment"] == enrollment
                and record["assignment"] == assignment
            ):
                record["marks"] = marks
                record["status"] = "Completed"

                new_remarks = self.remarks_entry.get().strip()

                if new_remarks:
                    record["remarks"] = new_remarks

                break

        self.save_data()
        self.refresh_table()

        messagebox.showinfo(
            "Success",
            "Marks updated successfully"
        )

    # -------------------------
    # Display selected record
    # -------------------------
    def load_selected_record(self, event=None):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0])["values"]

        self.enrollment_entry.delete(0, tk.END)
        self.enrollment_entry.insert(0, values[0])

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])

        self.assignment_entry.delete(0, tk.END)
        self.assignment_entry.insert(0, values[2])

        self.marks_entry.delete(0, tk.END)

        if values[4] != "":
            self.marks_entry.insert(0, values[4])

        self.remarks_entry.delete(0, tk.END)
        self.remarks_entry.insert(0, values[5])

    # -------------------------
    # Refresh table / Filtering
    # -------------------------
    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        selected_filter = self.filter_combo.get()

        for record in self.records:

            if (
                selected_filter != "All"
                and record["status"] != selected_filter
            ):
                continue

            self.tree.insert(
                "",
                tk.END,
                values=(
                    record["enrollment"],
                    record["name"],
                    record["assignment"],
                    record["status"],
                    record["marks"],
                    record["remarks"]
                )
            )

    # -------------------------
    # Clear fields
    # -------------------------
    def clear_fields(self):
        self.enrollment_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.assignment_entry.delete(0, tk.END)
        self.marks_entry.delete(0, tk.END)
        self.remarks_entry.delete(0, tk.END)

    # -------------------------
    # Export CSV
    # -------------------------
    def export_csv(self):
        if not self.records:
            messagebox.showerror(
                "Error",
                "No records to export"
            )
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )

        if not filename:
            return

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Enrollment",
                "Name",
                "Assignment",
                "Status",
                "Marks",
                "Remarks"
            ])

            for record in self.records:
                writer.writerow([
                    record["enrollment"],
                    record["name"],
                    record["assignment"],
                    record["status"],
                    record["marks"],
                    record["remarks"]
                ])

        messagebox.showinfo(
            "Success",
            "CSV report exported successfully"
        )


# -------------------------
# Start Application
# -------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = AssignmentManager(root)
    root.mainloop()