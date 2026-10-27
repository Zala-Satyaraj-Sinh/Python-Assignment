import sys

sys.setrecursionlimit(1000000)


class Parser:
    def __init__(self, text, variables):
        self.text = text
        self.variables = variables
        self.pos = 0

    def skip_spaces(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def parse(self):
        value = self.expression()
        self.skip_spaces()

        if self.pos != len(self.text):
            raise ValueError

        return value

    def expression(self):
        value = self.term()

        while True:
            self.skip_spaces()

            if self.pos >= len(self.text):
                break

            op = self.text[self.pos]

            if op not in "+-":
                break

            self.pos += 1
            right = self.term()

            if op == "+":
                value += right
            else:
                value -= right

        return value

    def term(self):
        value = self.factor()

        while True:
            self.skip_spaces()

            if self.pos >= len(self.text) or self.text[self.pos] != "*":
                break

            self.pos += 1
            value *= self.factor()

        return value

    def factor(self):
        self.skip_spaces()

        if self.pos >= len(self.text):
            raise ValueError

        ch = self.text[self.pos]

        # Number
        if ch.isdigit():
            start = self.pos

            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1

            return int(self.text[start:self.pos])

        # Parentheses
        if ch == "(":
            self.pos += 1
            value = self.expression()

            self.skip_spaces()

            if self.pos >= len(self.text) or self.text[self.pos] != ")":
                raise ValueError

            self.pos += 1
            return value

        # Variable
        if ch.isalpha() or ch == "_":
            start = self.pos
            self.pos += 1

            while (
                self.pos < len(self.text)
                and (self.text[self.pos].isalnum() or self.text[self.pos] == "_")
            ):
                self.pos += 1

            name = self.text[start:self.pos]

            if name not in self.variables:
                raise ValueError

            return evaluate_variable(name, self.variables)

        raise ValueError


# 0 = not visited
# 1 = currently evaluating
# 2 = already evaluated
state = {}
memo = {}


class CycleError(Exception):
    pass


def evaluate_variable(name, variables):
    if state[name] == 2:
        return memo[name]

    if state[name] == 1:
        raise CycleError

    state[name] = 1

    parser = Parser(variables[name], variables)
    value = parser.parse()

    memo[name] = value
    state[name] = 2

    return value


def main():
    lines = sys.stdin.buffer.read().decode().splitlines()

    try:
        v = int(lines[0].strip())

        if v < 1 or len(lines) != v + 2:
            print("INVALID")
            return

        variables = {}

        for i in range(1, v + 1):
            line = lines[i]

            if "=" not in line:
                print("INVALID")
                return

            name, expression = line.split("=", 1)

            name = name.strip()
            expression = expression.strip()

            if not name or name in variables:
                print("INVALID")
                return

            if not (
                name[0].isalpha() or name[0] == "_"
            ):
                print("INVALID")
                return

            if not all(
                ch.isalnum() or ch == "_"
                for ch in name
            ):
                print("INVALID")
                return

            variables[name] = expression
            state[name] = 0

        final_expression = lines[v + 1]

        parser = Parser(final_expression, variables)
        answer = parser.parse()

        print(answer)

    except CycleError:
        print("CYCLE")
    except (ValueError, RecursionError):
        print("INVALID")


if __name__ == "__main__":
    main()