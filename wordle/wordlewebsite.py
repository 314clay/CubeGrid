from flask import Flask, request, render_template

app = Flask(__name__)

# Load dictionary of English words
with open("words_alpha.txt") as f:
    word_set = set(f.read().split())

# Calculate letter frequency in English words
letter_freq = {'a': 0.0817, 'b': 0.0150, 'c': 0.0278, 'd': 0.0425, 'e': 0.1270,
               'f': 0.0223, 'g': 0.0202, 'h': 0.0609, 'i': 0.0697, 'j': 0.0015,
               'k': 0.0077, 'l': 0.0403, 'm': 0.0241, 'n': 0.0675, 'o': 0.0751,
               'p': 0.0193, 'q': 0.0010, 'r': 0.0599, 's': 0.0633, 't': 0.0906,
               'u': 0.0276, 'v': 0.0098, 'w': 0.0236, 'x': 0.0015, 'y': 0.0197, 'z': 0.0007}

# Define a function to calculate the score for a guess
def score_guess(guess, guesses):
    # Calculate letter frequency for the remaining letters
    remaining_letters = [c for c in "abcdefghijklmnopqrstuvwxyz" if c not in guesses]
    remaining_freq = {c: letter_freq[c] for c in remaining_letters}

    # Calculate the score for the guess
    score = 0
    for letter in guess:
        if letter in remaining_freq:
            score += remaining_freq[letter]
    return score

# Define the Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    guesses = set(request.form.getlist('guesses'))
    next_guess = None
    max_score = 0
    for word in word_set:
        if len(word) == 5 and set(word) <= guesses:
            score = score_guess(word, guesses)
            if score > max_score:
                next_guess = word
                max_score = score
    return render_template('result.html', next_guess=next_guess)

if __name__ == '__main__':
    app.run(debug=True)