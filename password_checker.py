import re


def load_common_passwords(file_path="common_passwords.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return set(line.strip().lower() for line in file if line.strip())
    except FileNotFoundError:
        return set()


def check_password_strength(password, common_passwords):
    score = 0
    feedback = []

    #Length Check
    if len(password) >= 12:
        score += 2
    elif len(password) >=8:
        score += 1
    else:
        feedback.append("Password is too short. Use at least 8 characters.")

    #Uppercase Check
    if re.search(r"[A-Z]", password):
        score +=1
    else:
        feedback.append("Add at least one uppercase letter.")

    #Lowercase Check
    if re.search(r"[a-z]", password):
        score +=1
    else:
        feedback.append("Add at least one lowercase letter.")

    #Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add at least one number.")

    #Special Character Check
    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\\/\[\]=+;']", password):
        score += 1
    else:
        feedback.append("Add at least one special character.")

    #Common Password Checker
    if password.lower() in common_passwords:
        score = max(score - 3,0)
        feedback.append("This password is too common and easily guessable.")

    #Repeated characters or patterns
    if re.search(r"(.)\1{2,}", password):
        score = max(score - 1, 0)
        feedback.append("Avoid repeated characters like 'aaa' or '111'")

    #Sequential pattern check
    sequences = ["123", "234", "345", "456", "567", "678", "789", "abc", "bcd", "cde", "qwerty"]
    for seq in sequences:
        if seq in password.lower():
            score = max(score - 1, 0)
            feedback.append("Avoid predictable sequences like '123' or 'abc'.")
            break

    #Final Rating
    if score <= 2:
        strength = "Very Weak"
    elif score <= 4:
        strength = "Weak"
    elif score <= 6:
        strength = "Moderate"
    else:
        strength = "Strong"

    return strength, score, feedback

def main():
    print("=== Password Strength Checker ===")
    common_passwords = load_common_passwords()

    password = input("Enter a password to check: ")
    strength, score, feedback = check_password_strength(password, common_passwords)

    print("\n--- Results ---")
    print(f"Password Strength: {strength}")
    print(f"Score: {score}/7")

    if feedback:
        print("\nSuggestions:")
        for item in feedback:
            print(f"- {item}")

    else:
        print("\nExcellent Password. No major weaknesses found.")

if __name__ == "__main__":
    main()


