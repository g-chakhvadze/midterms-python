

"""
მარტივი კალკულატორი — ძირითადი არითმეტიკული მოქმედებებით (+, -, *, /)
და შეყვანის ვალიდაციით.
"""
 
 
def get_number(prompt):
    """სთხოვს მომხმარებელს რიცხვს და ამოწმებს სისწორეს."""
    while True:
        raw = input(prompt).strip().replace(',', '.')
        try:
            return float(raw)
        except ValueError:
            print("შეცდომა: გთხოვთ შეიყვანოთ ვალიდური რიცხვი (მაგ: 3.14)")
 
 
def get_operation():
    """სთხოვს მომხმარებელს ოპერაციის არჩევას."""
    valid_ops = {'+', '-', '*', '/'}
    while True:
        op = input("აირჩიეთ მოქმედება (+, -, *, /): ").strip()
        if op in valid_ops:
            return op
        print("შეცდომა: მოქმედება უნდა იყოს ერთ-ერთი: +, -, *, /")
 
 
def calculate(a, b, op):
    """ასრულებს არჩეულ არითმეტიკულ მოქმედებას ორ რიცხვზე."""
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            raise ZeroDivisionError("ნულზე გაყოფა დაუშვებელია")
        return a / b
    else:
        raise ValueError(f"უცნობი მოქმედება: {op}")
 
 
def format_result(value):
    """ამრგვალებს შედეგს და შლის ზედმეტ ათწილადებს."""
    rounded = round(value, 8)
    if rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)
 
 
def main():
    print("=== კალკულატორი ===")
    while True:
        num1 = get_number("შეიყვანეთ პირველი რიცხვი: ")
        num2 = get_number("შეიყვანეთ მეორე რიცხვი: ")
        op = get_operation()
 
        try:
            result = calculate(num1, num2, op)
            print(f"შედეგი: {num1} {op} {num2} = {format_result(result)}")
        except ZeroDivisionError as e:
            print(f"შეცდომა: {e}")
        except ValueError as e:
            print(f"შეცდომა: {e}")
 
        again = input("გსურთ კიდევ ერთი გამოთვლა? (კი/არა): ").strip().lower()
        if again not in ('კი', 'yes', 'y', 'დიახ'):
            print("ნახვამდის!")
            break
 
 
if __name__ == "__main__":
    main()
 
