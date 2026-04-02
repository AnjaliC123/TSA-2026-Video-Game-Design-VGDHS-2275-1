import os
from random import randrange, choices
import string

# =========================
# ASCII ART
# =========================

TITLE = r"""
 __     __   ___    ___   ___    ___   ___   ___   ___
 \ \   / /  / _ \  / __| / _ \  | _ \ |   \ |_ _| / _ \
  \ \ / /  | (_) || (__ | (_) | |   / | |) | | | | (_) |
   \___/    \___/  \___|/_/*\_\ |_|_\ |___/ |___| \___/
                     V O C A R D I O
"""

YOGA_POSES = [
r"""
   O
  /|\
   |
  / \
""",
r"""
   O/|
   |/
   |_
 _/  \
""",
r"""
   O
 _/|\_
  /_\
""",
r"""
   O
  \|/
   |
  / \
""",
r"""
   O
  \|/
  /|
  \|
""",
r"""

   ___
 O|   |_

""",
r"""
    _
   / \
 O|  _\
""",
r"""

   __
 O|_ /_

"""
]

# FUNCTIONS

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def encrypt(scoreline, key):
    prepend = ''.join(choices(string.ascii_letters, k=5))
    scoreline = prepend + scoreline
    encrypted = ""
    for i in range(len(scoreline)):
        enccode = ord(scoreline[i]) + (ord(key[i])) - 64
        if enccode > 122: enccode -= 91
        encrypted += chr(enccode)
    return encrypted

def decrypt(encrypted, key):
    scoreline = ""
    for i in range(len(encrypted)):
        deccode = ord(encrypted[i]) - (ord(key[i])) + 64
        if deccode < 32: deccode += 91
        scoreline += chr(deccode)
    return scoreline[5:]

def Sort(scores):
    scores.sort(reverse=True, key=lambda x: x[1])
    return scores

# GAME SETUP

score = 0
hearts = 8
wordsdone = 0
guesses = []
message = "Welcome to Vocardio. Good luck! This is a "

file = open("wlist.txt", "r")
content = file.readlines()
file.close()

def load_word():
    global currword, info1, info2, sentence, currentguess
    wordnum = randrange(len(content)//4)

    currword = content[wordnum*4].strip().upper()
    info1 = content[wordnum*4+1].strip().upper()
    info2 = content[wordnum*4+2].strip().upper()
    sentence = content[wordnum*4+3].strip().upper()

    sentence = sentence.replace(currword, "*"*len(currword))
    currentguess = "-"*len(currword)

load_word()

# MAIN LOOP

while True:
    clear()

    print(TITLE)
    print(message + "\n")

    # HANGMAN VISUAL
    print(YOGA_POSES[8 - hearts])

    print("FIND THE WORD:  ", " ".join(currentguess), f"({len(currword)})\n")
    print(info1)
    print(info2)
    print(sentence + "\n")

    print("Hearts:", "❤ "*hearts)
    print(f"\nWords Completed: {wordsdone}     Score: {score}\n")

    guess = input("Enter a letter (or QUIT): ").upper()

    if guess == "":
        continue

    if guess == "QUIT":
        message = "You quit the game.\n--- GAME OVER ---"
        break

    guess = guess[0]

    if guess in guesses:
        message = f"You already guessed {guess}"
        continue

    guesses.append(guess)

    if guess in currword:
        newguess = ""
        for i in range(len(currword)):
            if currword[i] == guess:
                newguess += guess
            else:
                newguess += currentguess[i]

        currentguess = newguess

        if currentguess == currword:
            message = f"Correct! The word was {currword}"

            score += 100 if hearts == 8 else hearts * 10
            hearts = 8
            wordsdone += 1
            guesses = []

            load_word()
        else:
            message = f"Yes, it contains {guess}"

    else:
        hearts -= 1
        message = f"No, {guess} is not in the word"

        if hearts == 0:
            message = f"You ran out of hearts! The word was {currword}\n--- GAME OVER ---"
            break

# END SCREEN

clear()
print(TITLE)
print(message)
print(f"\nFinal Score: {score}")
print(f"Words Completed: {wordsdone}")
