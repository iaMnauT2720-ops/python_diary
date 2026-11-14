questions = ("1. What has keys, yet no locks; space, yet no room; and you can enter, yet you can’t go inside?"
            ,"2. If you drop me, I’m sure to crack, but give me a smile, and I’ll always smile back. What am I?"
            ,"3. The more of this there is, the less you see. What is it?"
            ,"4. Forward I am heavy, but backward I am not. What am I?"
            ,"5. What belongs to you, but other people use it more than you do?")
options =(("A. A treasure chest", "B. A keyboard", "C. A maze", "D. A hotel lobby")
          ,("A. A mirror", "B. A glass cup", "C. An egg", "D. A phone screen")
          ,("A. Fog", "B. Smoke", "C. Darkness", "D. Dust")
          ,("A. A rock", "B. A ton", "C. A truck", "D. A log")
          ,("A. Your phone", "B. Your time", "C. Your name", "D. Your umbrella"))
answers = ("A","A","C","B","C")
guesses = []
score = 0
question_num = 0

for question in questions:
    print("-------------------------------------------------")
    print(question)
    for option in options[question_num]:
        print(option)
    guess = input("Enter the answer(A,B,C,D): ").upper()
    guesses.append(guess)
    if guess == answers[question_num]:
        print("Gioi lam con trai!")
        score += 1
    else:
        print("Sai roi thang ngu!")
        print(f"{answers[question_num]} moi dung")
    question_num += 1
print()
print("your total score is: ", score)
if score == 5:
    print("Ghe vay sao!")
elif score < 5 and score > 0:
    print("Cung binh thuong!")
else:
    print("Ngu vlllll!")