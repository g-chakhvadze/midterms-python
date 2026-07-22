import json
import os
 
DATA_FILE = "accounts.json"
 
 

 
def create_default_file_if_missing():
    """
    თუ JSON ფაილი არ არსებობს, შექმენი ცარიელი ფაილი ({}).
    რეალურ სისტემაში არ არის სწორი, რომ პროგრამამ თავად "გამოიგონოს"
    სატესტო ანგარიშები და ფული — ანგარიშები უნდა დაემატოს მხოლოდ
    ადმინისტრატორის ან რეგისტრაციის პროცესის მეშვეობით.
    """
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        print(f"ℹ  შეიქმნა ცარიელი მონაცემთა ფაილი '{DATA_FILE}'. ჯერ არცერთი ანგარიში არ არსებობს.")
 
 
def load_accounts():
    """კითხულობს ანგარიშებს JSON ფაილიდან და აბრუნებს dictionary-ს."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
 
 
def save_accounts(accounts):
    """ინახავს ანგარიშებს (dictionary) JSON ფაილში."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(accounts, f, ensure_ascii=False, indent=2)
 
 
# ---------------------------------------------------------------------------
# ავტორიზაცია
# ---------------------------------------------------------------------------
 
def authenticate(accounts):
    print("\n=== ავტორიზაცია ===")
    acc_number = input("შეიყვანეთ ანგარიშის ნომერი: ").strip()
 
    if acc_number not in accounts:
        print(" ასეთი ანგარიში ვერ მოიძებნა.")
        return None
 
    attempts = 3
    while attempts > 0:
        pin = input("შეიყვანეთ PIN-კოდი: ").strip()
        if pin == accounts[acc_number]["pin"]:
            print(f" წარმატებული ავტორიზაცია. მოგესალმებით, ანგარიში #{acc_number}!")
            return acc_number
        else:
            attempts -= 1
            print(f" არასწორი PIN-კოდი. დარჩენილია მცდელობა: {attempts}")
 
    print("ავტორიზაცია ვერ განხორციელდა. ბარათი დაბლოკილია.")
    return None
 
 
# ---------------------------------------------------------------------------
# ბანკომატის ოპერაციები
# ---------------------------------------------------------------------------
 
def check_balance(accounts, acc_number):
    balance = accounts[acc_number]["balance"]
    print(f"\n💰 თქვენი მიმდინარე ბალანსია: {balance:.2f} ₾")
 
 
def deposit_money(accounts, acc_number):
    print("\n=== თანხის შეტანა ===")
    try:
        amount = float(input("შეიყვანეთ შესატანი თანხა: "))
    except ValueError:
        print(" არასწორი მნიშვნელობა. გთხოვთ, შეიყვანოთ რიცხვი.")
        return
 
    if amount <= 0:
        print(" თანხა უნდა იყოს დადებითი რიცხვი.")
        return
 
    accounts[acc_number]["balance"] += amount
    save_accounts(accounts)
    print(f" შეტანილია {amount:.2f} ₾. ახალი ბალანსი: {accounts[acc_number]['balance']:.2f} ₾")
 
 
def withdraw_money(accounts, acc_number):
    print("\n=== თანხის გატანა ===")
    try:
        amount = float(input("შეიყვანეთ გასატანი თანხა: "))
    except ValueError:
        print(" არასწორი მნიშვნელობა. გთხოვთ, შეიყვანოთ რიცხვი.")
        return
 
    if amount <= 0:
        print(" თანხა უნდა იყოს დადებითი რიცხვი.")
        return
 
    current_balance = accounts[acc_number]["balance"]
    if amount > current_balance:
        print(f" არასაკმარისი თანხა ანგარიშზე. თქვენი ბალანსია: {current_balance:.2f} ₾")
        return
 
    accounts[acc_number]["balance"] -= amount
    save_accounts(accounts)
    print(f" გატანილია {amount:.2f} ₾. ახალი ბალანსი: {accounts[acc_number]['balance']:.2f} ₾")
 
 
def change_pin(accounts, acc_number):
    print("\n=== PIN-კოდის შეცვლა ===")
    old_pin = input("შეიყვანეთ ძველი PIN-კოდი: ").strip()
    if old_pin != accounts[acc_number]["pin"]:
        print(" არასწორი ძველი PIN-კოდი.")
        return
 
    new_pin = input("შეიყვანეთ ახალი PIN-კოდი (4 ციფრი): ").strip()
    if len(new_pin) != 4 or not new_pin.isdigit():
        print(" PIN-კოდი უნდა შედგებოდეს ზუსტად 4 ციფრისგან.")
        return
 
    accounts[acc_number]["pin"] = new_pin
    save_accounts(accounts)
    print(" PIN-კოდი წარმატებით შეიცვალა.")
 
 
# ---------------------------------------------------------------------------
# მთავარი მენიუ
# ---------------------------------------------------------------------------
 
def main_menu(accounts, acc_number):
    while True:
        print("\n========= ბანკომატის მენიუ =========")
        print("1. ბალანსის შემოწმება")
        print("2. თანხის შეტანა")
        print("3. თანხის გატანა")
        print("4. PIN-კოდის შეცვლა")
        print("5. გასვლა")
        choice = input("აირჩიეთ ოპერაცია (1-5): ").strip()
 
        if choice == "1":
            check_balance(accounts, acc_number)
        elif choice == "2":
            deposit_money(accounts, acc_number)
        elif choice == "3":
            withdraw_money(accounts, acc_number)
        elif choice == "4":
            change_pin(accounts, acc_number)
        elif choice == "5":
            print("\n🙏 გმადლობთ, რომ ისარგებლეთ ბანკომატით. დაბრუნეთ ბარათი!")
            break
        else:
            print(" არასწორი არჩევანი. სცადეთ თავიდან.")
 
 
def main():
    print("=====================================")
    print("      კეთილი იყოს თქვენი მობრძანება   ")
    print("           ბანკომატის სისტემაში        ")
    print("=====================================")
 
    create_default_file_if_missing()
 
    while True:
        accounts = load_accounts()
        acc_number = authenticate(accounts)
 
        if acc_number:
            main_menu(accounts, acc_number)
 
        again = input("\nგსურთ სხვა ანგარიშით შესვლა? (დიახ/არა): ").strip().lower()
        if again not in ("დიახ", "კი", "yes", "y"):
            print("\n👋 პროგრამა დასრულდა. ნახვამდის!")
            break
 
 
if __name__ == "__main__":
    main()
 