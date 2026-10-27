class InvalidFormatError(Exception):
    pass


class UnknownVariableError(Exception):
    pass


class DivisionByZeroError(Exception):
    pass


class UnsupportedOperatorError(Exception):
    pass


class Calculator:
    def __init__(self):
        self.variables = {}

    def get_value(self, operand):
        # Try integer/decimal
        try:
            return float(operand)
        except ValueError:
            pass

        # Variable
        if operand in self.variables:
            return self.variables[operand]

        raise UnknownVariableError(
            f"Unknown variable: {operand}"
        )

    def assign(self, line):
        parts = line.split("=")

        if len(parts) != 2:
            raise InvalidFormatError("Invalid assignment format")

        name = parts[0].strip()
        value = parts[1].strip()

        if not name.isidentifier():
            raise InvalidFormatError("Invalid variable name")

        if not value:
            raise InvalidFormatError("Missing value")

        self.variables[name] = self.get_value(value)

    def calculate(self, line):
        parts = line.split()

        # Must be: operand operator operand
        if len(parts) != 3:
            raise InvalidFormatError(
                "Formula must be: operand operator operand"
            )

        left, operator, right = parts

        a = self.get_value(left)
        b = self.get_value(right)

        if operator == "+":
            return a + b

        elif operator == "-":
            return a - b

        elif operator == "*":
            return a * b

        elif operator == "/":
            if b == 0:
                raise DivisionByZeroError(
                    "Cannot divide by zero"
                )
            return a / b

        elif operator == "%":
            if b == 0:
                raise DivisionByZeroError(
                    "Cannot take modulo by zero"
                )
            return a % b

        else:
            raise UnsupportedOperatorError(
                f"Unsupported operator: {operator}"
            )


def format_result(value):
    # Print 15 instead of 15.0
    if value.is_integer():
        return str(int(value))
    return str(value)


def main():
    calculator = Calculator()

    while True:
        try:
            line = input().strip()

            if line.lower() == "quit":
                break

            if not line:
                continue

            # Assignment
            if "=" in line:
                calculator.assign(line)

            # Formula
            else:
                result = calculator.calculate(line)
                print(format_result(result))

        except DivisionByZeroError:
            print("DivisionByZeroError")

        except UnsupportedOperatorError:
            print("UnsupportedOperatorError")

        except UnknownVariableError:
            print("UnknownVariableError")

        except InvalidFormatError:
            print("InvalidFormatError")


if __name__ == "__main__":
    main()