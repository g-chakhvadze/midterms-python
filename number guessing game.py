

"""
"გამოიცანი რიცხვი" — თამაში, სადაც პროგრამა გენერირებს შემთხვევით
რიცხვს მითითებულ დიაპაზონში და მომხმარებელი უნდა გამოიცნოს ის,
მინიშნებების (მეტი/ნაკლები) დახმარებით.
"""
 
import random
 
 
def get_range():
    """სთხოვს მომხმარებელს დიაპაზონის საზღვრებს და ამოწმებს სისწორეს."""
    while True:
        try:
            low = int(input("შეიყვანეთ დიაპაზონის ქვედა ზღვარი: ").strip())
            high = int(input("შეიყვანეთ დიაპაზონის ზედა ზღვარი: ").strip())
        except ValueError:
            print("შეცდომა: გთხოვთ შეიყვანოთ მთელი რიცხვები\n")
            continue
 
        if low >= high:
            print("შეცდომა: ქვედა ზღვარი უნდა იყოს ზედაზე ნაკლები\n")
            continue
 
        return low, high
 
 
def get_guess(low, high):
    """სთხოვს მომხმარებელს ვარაუდს და ამოწმებს, რომ ის მთელი რიცხვია დიაპაზონში."""
    while True:
        raw = input(f"შეიყვანეთ თქვენი ვარაუდი ({low}-{high}): ").strip()
        try:
            guess = int(raw)
        except ValueError:
            print("შეცდომა: გთხოვთ შეიყვანოთ მთელი რიცხვი")
            continue
 
        if guess < low or guess > high:
            print(f"შეცდომა: რიცხვი უნდა იყოს {low}-დან {high}-მდე")
            continue
 
        return guess
 
 
def play_round(low, high):
    """თამაშობს ერთ რაუნდს და აბრუნებს გამოყენებული მცდელობების რაოდენობას."""
    target = random.randint(low, high)
    attempts = 0
 
    print(f"\nგამოიცანით რიცხვი {low}-დან {high}-მდე დიაპაზონში!")
 
    while True:
        guess = get_guess(low, high)
        attempts += 1
 
        if guess < target:
            print("მინიშნება: უფრო მაღალი რიცხვი სცადეთ\n")
        elif guess > target:
            print("მინიშნება: უფრო დაბალი რიცხვი სცადეთ\n")
        else:
            print(f"\nგილოცავთ! გამოიცანით რიცხვი {target} — {attempts} მცდელობაში!")
            return attempts
 
 
def main():
    print("=== გამოიცანი რიცხვი ===")
    while True:
        low, high = get_range()
        play_round(low, high)
 
        again = input("\nგსურთ კიდევ ერთხელ თამაში? (კი/არა): ").strip().lower()
        if again not in ('კი', 'yes', 'y', 'დიახ'):
            print("ნახვამდის!")
            break
        print()
 
 
if __name__ == "__main__":
    main()
 
