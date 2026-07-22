import json
import os


class Account:
    def __init__(self, account_number, pin, balance=0.0):
        self.account_number = account_number
        self.pin = pin
        self.balance = float(balance)

    def verify_pin(self, pin_attempt):
        return self.pin == pin_attempt

    def check_balance(self):
        return self.balance

    def deposit(self, amount):
        if amount <= 0:
            return False, "თანხა უნდა იყოს დადებითი რიცხვი."
        self.balance += amount
        return True, f"შეტანილია {amount:.2f} ₾. ახალი ბალანსი: {self.balance:.2f} ₾"

    def withdraw(self, amount):
        if amount <= 0:
            return False, "თანხა უნდა იყოს დადებითი რიცხვი."
        if amount > self.balance:
            return False, f"არასაკმარისი თანხა. თქვენი ბალანსია: {self.balance:.2f} ₾"
        self.balance -= amount
        return True, f"გატანილია {amount:.2f} ₾. ახალი ბალანსი: {self.balance:.2f} ₾"

    def change_pin(self, old_pin, new_pin):
        if old_pin != self.pin:
            return False, "არასწორი ძველი PIN-კოდი."
        if len(new_pin) != 4 or not new_pin.isdigit():
            return False, "PIN-კოდი უნდა შედგებოდეს ზუსტად 4 ციფრისგან."
        self.pin = new_pin
        return True, "PIN-კოდი წარმატებით შეიცვალა."

    def to_dict(self):
        return {"pin": self.pin, "balance": self.balance}

    @classmethod
    def from_dict(cls, account_number, data):
        return cls(account_number, data["pin"], data["balance"])


class ATM:
    def __init__(self, data_file="accounts.json"):
        self.data_file = data_file
        self.accounts = {}
        self._ensure_file_exists()
        self.load_accounts()

    def _ensure_file_exists(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            print(f"ℹ️  შეიქმნა ცარიელი მონაცემთა ფაილი '{self.data_file}'. ჯერ არცერთი ანგარიში არ არსებობს.")

    def load_accounts(self):
        with open(self.data_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        self.accounts = {
            acc_number: Account.from_dict(acc_number, info)
            for acc_number, info in raw_data.items()
        }

    def save_accounts(self):
        raw_data = {
            acc_number: account.to_dict()
            for acc_number, account in self.accounts.items()
        }
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=2)

    def authenticate(self):
        print("\n=== ავტორიზაცია ===")
        acc_number = input("შეიყვანეთ ანგარიშის ნომერი: ").strip()

        account = self.accounts.get(acc_number)
        if account is None:
            print("❌ ასეთი ანგარიში ვერ მოიძებნა.")
            return None

        attempts = 3
        while attempts > 0:
            pin = input("შეიყვანეთ PIN-კოდი: ").strip()
            if account.verify_pin(pin):
                print(f"✅ წარმატებული ავტორიზაცია. მოგესალმებით, ანგარიში #{acc_number}!")
                return account
            attempts -= 1
            print(f"❌ არასწორი PIN-კოდი. დარჩენილია მცდელობა: {attempts}")

        print("ავტორიზაცია ვერ განხორციელდა. ბარათი დაბლოკილია.")
        return None

    def _handle_check_balance(self, account):
        print(f"\n💰 თქვენი მიმდინარე ბალანსია: {account.check_balance():.2f} ₾")

    def _handle_deposit(self, account):
        print("\n=== თანხის შეტანა ===")
        try:
            amount = float(input("შეიყვანეთ შესატანი თანხა: "))
        except ValueError:
            print("❌ არასწორი მნიშვნელობა. გთხოვთ, შეიყვანოთ რიცხვი.")
            return

        success, message = account.deposit(amount)
        print(("✅ " if success else "❌ ") + message)
        if success:
            self.save_accounts()

    def _handle_withdraw(self, account):
        print("\n=== თანხის გატანა ===")
        try:
            amount = float(input("შეიყვანეთ გასატანი თანხა: "))
        except ValueError:
            print("❌ არასწორი მნიშვნელობა. გთხოვთ, შეიყვანოთ რიცხვი.")
            return

        success, message = account.withdraw(amount)
        print(("✅ " if success else "❌ ") + message)
        if success:
            self.save_accounts()

    def _handle_change_pin(self, account):
        print("\n=== PIN-კოდის შეცვლა ===")
        old_pin = input("შეიყვანეთ ძველი PIN-კოდი: ").strip()
        new_pin = input("შეიყვანეთ ახალი PIN-კოდი (4 ციფრი): ").strip()

        success, message = account.change_pin(old_pin, new_pin)
        print(("✅ " if success else "❌ ") + message)
        if success:
            self.save_accounts()

    def main_menu(self, account):
        while True:
            print("\n========= ბანკომატის მენიუ =========")
            print("1. ბალანსის შემოწმება")
            print("2. თანხის შეტანა")
            print("3. თანხის გატანა")
            print("4. PIN-კოდის შეცვლა")
            print("5. გასვლა")
            choice = input("აირჩიეთ ოპერაცია (1-5): ").strip()

            if choice == "1":
                self._handle_check_balance(account)
            elif choice == "2":
                self._handle_deposit(account)
            elif choice == "3":
                self._handle_withdraw(account)
            elif choice == "4":
                self._handle_change_pin(account)
            elif choice == "5":
                print("\n🙏 გმადლობთ, რომ ისარგებლეთ ბანკომატით. დაბრუნეთ ბარათი!")
                break
            else:
                print("❌ არასწორი არჩევანი. სცადეთ თავიდან.")

    def run(self):
        print("=====================================")
        print("      კეთილი იყოს თქვენი მობრძანება   ")
        print("           ბანკომატის სისტემაში        ")
        print("=====================================")

        while True:
            self.load_accounts()
            account = self.authenticate()

            if account:
                self.main_menu(account)

            again = input("\nგსურთ სხვა ანგარიშით შესვლა? (დიახ/არა): ").strip().lower()
            if again not in ("დიახ", "კი", "yes", "y"):
                print("\n👋 პროგრამა დასრულდა. ნახვამდის!")
                break


if __name__ == "__main__":
    atm = ATM(data_file="accounts.json")
    atm.run()