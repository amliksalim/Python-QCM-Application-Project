import json
from datetime import datetime

def load_data(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

def signup(users_file):
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    users = load_data(users_file)
    if email in users:
        print("Email already registered. Please login.")
        return False
    else:
        users[email] = {"name": name, "password": password, "history": []}
        save_data(users_file, users)
        print("Signup successful! Please login.")
        return True

def login(users_file):
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    users = load_data(users_file)
    if email in users and users[email]['password'] == password:
        print("Login successful!")
        return email
    else:
        print("Invalid email or password.")
        return None

def show_history(user_data):
    if user_data["history"]:
        print("\n--- Your History ---")
        for record in user_data["history"]:
            print(f"Date: {record['date']}, Category: {record['category']}, Score: {record['score']}")
    else:
        print("No history available.")

def take_quiz(user_email, users_file, questions_file):
    categories = {"1": "Linux", "2": "Python", "3": "AI", "4": "HTML/CSS", "5": "Node.js"}
    print("\nChoose a category:")
    for key, value in categories.items():
        print(f"{key}- {value}")

    choice = input("Enter your preference: ")
    if choice not in categories:
        print("Invalid choice.")
        return

    category = categories[choice]
    questions = load_data(questions_file).get(category, [])
    if not questions:
        print(f"No questions available for {category}.")
        return

    score = 0
    for i, question in enumerate(questions[:7], start=1):
        print(f"\nQ{i}: {question['question']}")
        for index, option in enumerate(question['options'], start=1):
            print(f"{index}- {option}")
        answer = input("Your answer: ").strip()
        if answer == question['answer']:
            score += 1

    print(f"\nYou completed the quiz! Your score: {score}/{len(questions[:7])}")

    users = load_data(users_file)
    users[user_email]["history"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "score": score
    })
    save_data(users_file, users)

def main():
    users_file = "users.json"
    questions_file = "questions.json"

    while True:
        print("\n--- Welcome ---")
        print("1- Login")
        print("2- Signup")
        print("3- Exit")

        choice = input("What do you like to do: ")
        if choice=="3":
            print("Thank you for using our quiz system. Goodbye!")
            break
        elif choice == "2":
            if signup(users_file):
                continue
        elif choice == "1":
            user_email = login(users_file)
            if user_email:
                while True:
                    print("\n1- See History")
                    print("2- Test Your Knowledge")
                    print("3- Exit")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        user_data = load_data(users_file).get(user_email)
                        show_history(user_data)
                    elif choice == "2":
                        take_quiz(user_email, users_file, questions_file)
                    elif choice=="3":
                        break
                    else:
                        print("Invalid choice.")
            else:
                continue
        else:
            print("Invalid choice.")


main()
