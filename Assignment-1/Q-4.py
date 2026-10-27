import csv
from decimal import Decimal, InvalidOperation
from datetime import datetime


def validate_row(row):
    # Check required fields
    required = ["tid", "acc", "type", "amount", "time"]

    for field in required:
        if field not in row or not row[field].strip():
            raise ValueError(f"missing {field}")

    tid = row["tid"].strip()
    acc = row["acc"].strip()
    trans_type = row["type"].strip().upper()
    amount_text = row["amount"].strip()
    timestamp = row["time"].strip()

    # Validate transaction type
    if trans_type not in ("CREDIT", "DEBIT"):
        raise ValueError("invalid transaction type")

    # Validate amount
    try:
        amount = Decimal(amount_text)
    except InvalidOperation:
        raise ValueError("amount is not numeric")

    if amount <= 0:
        raise ValueError("amount must be greater than 0")

    # Validate timestamp
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise ValueError("invalid timestamp")

    return {
        "tid": tid,
        "acc": acc,
        "type": trans_type,
        "amount": amount,
        "time": timestamp
    }


def main():
    input_file = input("Enter CSV file path: ").strip()

    balances = {}

    header = ["tid", "acc", "type", "amount", "time"]

    try:
        with open(input_file, "r", newline="", encoding="utf-8") as infile, \
             open("credit.csv", "w", newline="", encoding="utf-8") as credit_file, \
             open("debit.csv", "w", newline="", encoding="utf-8") as debit_file, \
             open("error.csv", "w", newline="", encoding="utf-8") as error_file:

            reader = csv.DictReader(infile)

            credit_writer = csv.DictWriter(
                credit_file,
                fieldnames=header
            )

            debit_writer = csv.DictWriter(
                debit_file,
                fieldnames=header
            )

            error_writer = csv.writer(error_file)

            credit_writer.writeheader()
            debit_writer.writeheader()
            error_writer.writerow(header + ["reason"])

            for row in reader:
                try:
                    data = validate_row(row)

                    # Convert Decimal back to string for CSV
                    output_row = {
                        "tid": data["tid"],
                        "acc": data["acc"],
                        "type": data["type"],
                        "amount": str(data["amount"]),
                        "time": data["time"]
                    }

                    if data["type"] == "CREDIT":
                        credit_writer.writerow(output_row)
                        balances[data["acc"]] = (
                            balances.get(data["acc"], Decimal("0"))
                            + data["amount"]
                        )

                    else:
                        debit_writer.writerow(output_row)
                        balances[data["acc"]] = (
                            balances.get(data["acc"], Decimal("0"))
                            - data["amount"]
                        )

                except Exception as e:
                    error_writer.writerow([
                        row.get("tid", ""),
                        row.get("acc", ""),
                        row.get("type", ""),
                        row.get("amount", ""),
                        row.get("time", ""),
                        str(e)
                    ])

    except FileNotFoundError:
        print("Input file not found.")
        return

    except Exception as e:
        print("File error:", e)
        return

    # Sort by descending absolute balance change
    result = sorted(
        balances.items(),
        key=lambda x: (-abs(x[1]), x[0])
    )

    print("\nAccount-wise balance changes:")

    for account, balance in result:
        # Remove unnecessary .0
        if balance == balance.to_integral():
            print(account, int(balance))
        else:
            print(account, balance)


if __name__ == "__main__":
    main()