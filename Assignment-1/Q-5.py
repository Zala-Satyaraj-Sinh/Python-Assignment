class BankError(Exception):
    pass


class AccountNotFound(BankError):
    pass


class InsufficientFunds(BankError):
    pass


class InvalidAmount(BankError):
    pass


class Account:
    def __init__(self, account_id, balance=0):
        self.account_id = account_id
        self._balance = balance
        self.history = []

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmount

        self._balance += amount
        self.history.append(("DEPOSIT", amount))

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmount

        if amount > self._balance:
            raise InsufficientFunds

        self._balance -= amount
        self.history.append(("WITHDRAW", amount))

    def set_balance(self, balance):
        self._balance = balance


class Transaction:
    def __init__(self, operation, *args):
        self.operation = operation
        self.args = args


class Bank:
    def __init__(self):
        self.accounts = {}

    def add_account(self, account_id, balance):
        self.accounts[account_id] = Account(account_id, balance)

    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFound
        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)
        account.deposit(amount)

    def withdraw(self, account_id, amount):
        account = self.get_account(account_id)
        account.withdraw(amount)

    def transfer(self, from_id, to_id, amount):
        source = self.get_account(from_id)
        destination = self.get_account(to_id)

        if amount <= 0:
            raise InvalidAmount

        if amount > source.balance:
            raise InsufficientFunds

        # Perform transfer
        source._balance -= amount
        destination._balance += amount

        source.history.append(("TRANSFER_OUT", amount, to_id))
        destination.history.append(("TRANSFER_IN", amount, from_id))


def main():
    bank = Bank()

    # Number of accounts
    n = int(input())

    for _ in range(n):
        account_id, balance = input().split()
        bank.add_account(account_id, int(balance))

    # Number of operations
    q = int(input())

    in_batch = False
    batch_number = 0
    failed_batches = []

    # Stores old balance + history length
    # for every modification in the current batch.
    batch_changes = []

    for _ in range(q):
        parts = input().split()

        if not parts:
            continue

        operation = parts[0]

        # Start batch
        if operation == "BATCH_BEGIN":
            in_batch = True
            batch_number += 1
            batch_changes = []
            continue

        # End batch
        if operation == "BATCH_END":
            in_batch = False
            batch_changes = []
            continue

        try:
            # Save state before operation
            if in_batch:
                affected = []

                if operation == "DEPOSIT":
                    affected = [parts[1]]

                elif operation == "WITHDRAW":
                    affected = [parts[1]]

                elif operation == "TRANSFER":
                    affected = [parts[1], parts[2]]

                # Store previous state
                for account_id in affected:
                    account = bank.get_account(account_id)

                    batch_changes.append((
                        account,
                        account.balance,
                        len(account.history)
                    ))

            # Execute operation
            if operation == "DEPOSIT":
                account_id = parts[1]
                amount = int(parts[2])

                bank.deposit(account_id, amount)

            elif operation == "WITHDRAW":
                account_id = parts[1]
                amount = int(parts[2])

                bank.withdraw(account_id, amount)

            elif operation == "TRANSFER":
                from_id = parts[1]
                to_id = parts[2]
                amount = int(parts[3])

                bank.transfer(from_id, to_id, amount)

            else:
                raise BankError

        except (BankError, ValueError, IndexError):

            if in_batch:
                # Roll back every operation in reverse order
                for account, old_balance, old_history_size in reversed(batch_changes):
                    account.set_balance(old_balance)
                    del account.history[old_history_size:]

                failed_batches.append(batch_number)

                # Batch is considered completed/rolled back
                in_batch = False
                batch_changes = []

    # Print failed batches
    for number in failed_batches:
        print("FAILED", number)

    # Final balances in account ID order
    for account_id in sorted(bank.accounts):
        account = bank.accounts[account_id]
        print(account_id, account.balance)


if __name__ == "__main__":
    main()