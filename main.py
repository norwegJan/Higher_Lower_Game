# import modules
import os
import art
import random
import readchar
import game_data

# assign globals
WINNER_SCORE = 25

# define functions
def initialize_alternatives():
    """Returns a list with two unique random profiles from game_data.data"""

    alternatives = []
    alt_0 = random.choice(game_data.data)
    alt_1 = random.choice(game_data.data)

    while alt_1 == alt_0:
        alt_1 = random.choice(game_data.data)

    alternatives.append(alt_0)
    alternatives.append(alt_1)

    return alternatives

def get_user_guess():
    """Reads input from user and returns a string letter, 'A' or 'B', reflecting user's guess"""

    while True:
        print("Who has more followers? Press A/◀️-arrow for 'A', or B/▶️-arrow for 'B':")
        user_guess = readchar.readkey()
        if user_guess in ['a', 'A', readchar.key.LEFT]:
            return 'A'
        elif user_guess in ['b', 'B', readchar.key.RIGHT]:
            return 'B'
        else:
            print("Invalid input!")

def is_guess_correct(guess, alternatives):
    """Takes in two values: user's guess and the alternatives-list.
    Checks whether user have guessed correct profile and returns either True or False"""

    if guess == 'A':
        user_answer = alternatives[0]['follower_count']
    elif guess == 'B':
        user_answer = alternatives[1]['follower_count']

    correct_answer = max(alternatives[0]['follower_count'], alternatives[1]['follower_count'])

    if user_answer == correct_answer:
        return True
    else:
        return False

def update_alternatives(alternatives, quarantine):
    """
    Takes in two values: the current alternatives-list and the current quarantine-list and updates the profiles in the lists directly.
    The previous alternative B becomes the new alternative A.
    """

    removed_alt = alternatives.pop(0)
    quarantine.append(removed_alt)

    if len(quarantine) > 5:
        quarantine.pop(0)

    alt_1 = random.choice(game_data.data)

    while alternatives[0] == alt_1 or alt_1 in quarantine:
        alt_1 = random.choice(game_data.data)

    alternatives.append(alt_1)

    return alternatives

def clear_screen():
    """Clears terminal with correct command depending on which OS is used"""

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# run main logic
run_game = True
new_round = False

print(art.logo)
print("\n---------- Welcome to the Higher Lower game! ⬆️ ⬇️  👋")
print("---------- FYI: You can play this game entirely with the ◀️ 🔼▶️ 🔽 arrow-keys!\n")

while run_game:

    while True:
        print("---------- Press 1/🔼-arrow to begin, or q/🔽-arrow to quit:\n")
        start_choice = readchar.readkey()
        if start_choice in ['1', readchar.key.UP, 'q', 'Q', readchar.key.DOWN]:
            break
        else:
            print("Invalid input!")

    if start_choice in ['1', readchar.key.UP]:
        new_round = True
        alternatives = initialize_alternatives()
        quarantine = []
        user_score = 0

    if start_choice in ['q', 'Q', readchar.key.DOWN]:
        run_game = False
        new_round = False
        print("Thank you for playing Higher Lower ver 1.0. Have a nice day!")

    while new_round:

        clear_screen()
        alt_A = alternatives[0]
        alt_B = alternatives[1]

        print(art.logo)

        if user_score > 0:
            print("---------- That's correct! 🤩 ----------")
            print(f"---------- Your score: ----- {user_score} -----\n")

        print("---------- 👇 Compare A and B! 👇 ----------\n")
        print(f"-----> A: {alt_A['name']}, a {alt_A['description'].lower()}, from {alt_A['country']}.")
        print(art.vs)
        print(f"-----> B: {alt_B['name']}, a {alt_B['description'].lower()}, from {alt_B['country']}.")
        print("")

        user_guess = get_user_guess()

        if not is_guess_correct(user_guess, alternatives):
            clear_screen()
            print(art.logo)
            print("\n---------- Bummer! You got it wrong! 😳----------")
            print(f"---------- You got a total score of: --- {user_score} ---\n")
            print("---------- Do you want to try another round?  ----------\n")
            new_round = False

        else:
            user_score += 1
            if user_score < WINNER_SCORE:
                update_alternatives(alternatives, quarantine)

            elif user_score == WINNER_SCORE:
                clear_screen()
                print(art.logo)
                print(f"\n---------- Wow! You reached the end with a total score of: ___ {user_score} ___  😮")
                print("---------- Only about 5% of players get this far! (unfortunately, there's no source for this claim) 🥳👏\n")
                print("---------- Do you want to try another round?  ----------\n")
                new_round = False
