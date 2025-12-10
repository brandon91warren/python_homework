def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter.lower())

        displayed = ""
        for char in secret_word:
            if char.lower() in guesses:
                displayed += char
            else:
                displayed += "_"

        print(displayed)

        return "_" not in displayed

    return hangman_closure


# ---------------------------
# MAIN GAME LOOP
# ---------------------------
if __name__ == "__main__":
    secret = input("Enter the secret word: ").strip()
    hangman = make_hangman(secret)

    print("\nLet's play Hangman!")
    print("_" * len(secret))

    while True:
        guess = input("Guess a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter ONE letter.")
            continue

        done = hangman(guess)

        if done:
            print("🎉 You guessed the word!")
            break
