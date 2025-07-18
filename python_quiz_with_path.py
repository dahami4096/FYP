# Step 1: Ask some Python questions

score = 0

print("Welcome to the Python Level Checker!")
print("Answer these 3 questions to find your skill level.")

# Question 1
answer1 = input("1. What is the output of: print(2 + 3 * 4)? ")
if answer1 == "14":
    score += 1

# Question 2
answer2 = input("2. What keyword is used to define a function in Python? ")
if answer2.lower() == "def":
    score += 1

# Question 3
answer3 = input("3. What does 'len()' do in Python? ")
if "length" in answer3.lower():
    score += 1

# Determine level
if score == 3:
    level = "Advanced"
elif score == 2:
    level = "Intermediate"
else:
    level = "Beginner"

print(f"\nYour Python level is: {level}")
# Suggest topics based on the user's level
print("\nHere's your personalized Python learning path:")

if level == "Beginner":
    topics = [
        "1. Variables and Data Types",
        "2. Print and Input",
        "3. If-Else Conditions",
        "4. Loops (while, for)",
        "5. Basic Functions"
    ]
elif level == "Intermediate":
    topics = [
        "1. Functions (parameters, return)",
        "2. Lists and Dictionaries",
        "3. File Handling (open, read, write)",
        "4. Error Handling (try-except)",
        "5. Working with Modules"
    ]
else:  # Advanced
    topics = [
        "1. Object-Oriented Programming (Classes & Objects)",
        "2. Recursion",
        "3. Generators and Iterators",
        "4. Decorators",
        "5. Working with APIs and JSON"
    ]

# Print the list
for topic in topics:
    print(topic)


